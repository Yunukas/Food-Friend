# chat_bot.py

import os
import json
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
APP_NAME = os.getenv('APP_NAME', 'Food Friend')

from llm_utils_updated import load_llm, extract_food_choices
from llm_hybrid_matcher import llm_hybrid_match

DATA_DIR = "data/users"
os.makedirs(DATA_DIR, exist_ok=True)

def user_file(name):
    safe = name.replace(" ", "_").lower()
    return os.path.join(DATA_DIR, f"user_{safe}.json")

def save_user_json(data):
    with open(user_file(data["name"]), "w") as f:
        json.dump(data, f, indent=2)

def load_all_users(exclude=None):
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

        if "name" not in data:
            continue
        if exclude and data["name"].lower() == exclude.lower():
            continue

        data.setdefault("foodChoices", [])
        users.append(data)

    return users


def main():
    print(f"Welcome to {APP_NAME}!")
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
        user.setdefault("name", name)
        user.setdefault("foodChoices", [])
        user.setdefault("userId", str(uuid.uuid4()))
        user.setdefault("createdAt", str(datetime.now()))
    else:
        print(f"Creating a new profile for {name}...\n")
        user = {
            "userId": str(uuid.uuid4()),
            "name": name,
            "foodChoices": [],
            "createdAt": str(datetime.now()),
            "lastUpdated": str(datetime.now())
        }

    llm = load_llm()

    print("\nDescribe your favorite foods or cuisines:")
    desc = input("> ").strip()

    choices = extract_food_choices(llm, desc)
    if not isinstance(choices, list):
        choices = []

    print("\nExtracted food choices:", choices)

    user["foodChoices"] = choices
    user["lastUpdated"] = str(datetime.now())
    save_user_json(user)

    print("\nSaved your preferences!")
    print("Finding your top matches...\n")

    others = load_all_users(exclude=name)
    if not others:
        print("No other users yet.")
        return

    # Hybrid LLM + Python scoring
    results = []
    for other in others:
        result = llm_hybrid_match(llm, user, other)
        results.append((other["name"], result))

    results.sort(key=lambda x: x[1]["final_score"], reverse=True)

    print("Top Matches:\n")
    for name, r in results[:5]:
        print(f"{name}: {r['final_score']}% match")
        print(f"  Python score: {r['python_score']}%")
        print(f"  LLM score: {r['llm_score']}%")
        print(f"  Reason: {r['reason']}")

        if r["matched_cuisines"]:
            print("  Matched cuisines:", ", ".join(r["matched_cuisines"]))
        if r["shared_exact"]:
            print("  Shared dishes:", ", ".join(r["shared_exact"]))
        if r["keyword_hits"]:
            print("  Keyword matches:", ", ".join(r["keyword_hits"]))
        print()

    print("Done!\n")


if __name__ == "__main__":
    main()
