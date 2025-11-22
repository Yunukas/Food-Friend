# draft_chat_bot.py

import os
import json
from datetime import datetime

from llm_utils import load_llm, extract_food_choices
from match_engine import score_pair

DATA_DIR = "data/users"
os.makedirs(DATA_DIR, exist_ok=True)

def user_file(name):
    safe = name.replace(" ", "_").lower()
    return os.path.join(DATA_DIR, f"user_{safe}.json")


def save_user_json(data):
    """
    Saves user JSON with guaranteed correct schema:
    {
      "name": "",
      "foodChoices": [],
      "createdAt": "",
      "lastUpdated": ""
    }
    """
    with open(user_file(data["name"]), "w") as f:
        json.dump(data, f, indent=2)


def load_all_users(exclude=None):
    """
    Loads all users except the current one.
    Ensures each loaded user has 'name' and 'foodChoices'.
    """
    users = []

    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".json"):
            continue

        path = os.path.join(DATA_DIR, fname)
        try:
            with open(path) as f:
                data = json.load(f)
        except:
            continue

        # Guarantee required fields
        if "name" not in data:
            continue

        if exclude and data["name"].lower() == exclude.lower():
            continue

        data.setdefault("foodChoices", [])
        users.append(data)

    return users


def main():
    print("🍽️ Welcome to Food-Friend!")
    name = input("Enter your name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    path = user_file(name)

    # Load or create profile
    if os.path.exists(path):
        print(f"Loaded existing profile for {name}\n")
        with open(path) as f:
            user = json.load(f)

        # Guarantee fields
        user.setdefault("name", name)
        user.setdefault("foodChoices", [])
        user.setdefault("createdAt", str(datetime.now()))
    else:
        print(f"Creating a new profile for {name}...\n")
        user = {
            "name": name,
            "foodChoices": [],
            "createdAt": str(datetime.now()),
            "lastUpdated": str(datetime.now())
        }

    # Load local LLM
    llm = load_llm()

    print("\nDescribe your favorite foods or cuisines:")
    desc = input("> ").strip()

    # Extract food choices (robust for Qwen 3B)
    choices = extract_food_choices(llm, desc)

    if not isinstance(choices, list):
        choices = []

    print("\nExtracted food choices:", choices)

    # Update user
    user["foodChoices"] = choices
    user["lastUpdated"] = str(datetime.now())
    save_user_json(user)

    print("\nSaved your preferences!")
    print("Finding your top matches...\n")

    # Load other users
    others = load_all_users(exclude=name)

    if not others:
        print("No other users yet. Add more profiles!")
        return

    # Score matches
    results = []
    for other in others:
        scoreinfo = score_pair(user, other)
        results.append((other["name"], scoreinfo))

    # Sort by descending score
    results.sort(key=lambda x: x[1]["score"], reverse=True)

    print("🔥 Top Matches:\n")
    for other_name, result in results[:3]:
        print(f"{other_name}: {result['score']}% match")

        # Show exact shared dishes
        if result.get("shared_exact"):
            print("  Shared exact dishes:", ", ".join(result["shared_exact"]))

        # Show matched cuisines
        if result.get("matched_cuisines"):
            print("  Matched cuisines:", ", ".join(result["matched_cuisines"]))

        # Show general keyword similarity
        if result.get("keyword_hits"):
            print("  Keyword similarity:", ", ".join(result["keyword_hits"]))

        print()  # spacing

    print("Done!\n")


if __name__ == "__main__":
    main()
