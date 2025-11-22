# draft_chat_bot.py
import os
import json
import uuid
from datetime import datetime

from llm_utils import load_llm, extract_food_choices
from match_engine import score_pair

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
        if fname.endswith(".json"):
            with open(os.path.join(DATA_DIR, fname)) as f:
                data = json.load(f)
                if exclude and data["name"].lower() == exclude.lower():
                    continue
                users.append(data)
    return users

def main():
    print("🍽️ Welcome to Food-Friend!")
    name = input("Enter your name: ").strip()

    # Guarantee name always exists
    if not name:
        print("Name cannot be empty.")
        return

    path = user_file(name)

    # Load OR create user JSON
    if os.path.exists(path):
        print(f"Loaded existing profile for {name}\n")
        with open(path) as f:
            user = json.load(f)

        # Guarantee essential fields
        user.setdefault("name", name)
        user.setdefault("foodChoices", [])
        user.setdefault("userId", str(uuid.uuid4()))

    else:
        print(f"Creating a new profile for {name}...\n")
        user = {
            "userId": str(uuid.uuid4()),
            "name": name,
            "foodChoices": [],
            "createdAt": str(datetime.now()),
            "lastUpdated": str(datetime.now()),
        }

    llm = load_llm()

    print("\nDescribe your favorite foods or cuisines:")
    desc = input("> ").strip()

    choices = extract_food_choices(llm, desc)

    # Guarantee extraction returns a list
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
        print("No other users yet. Add more profiles!")
        return

    results = []
    for other in others:
        results.append((other["name"], score_pair(user, other)))

    # Sort by score
    results.sort(key=lambda x: x[1]["score"], reverse=True)

    print("🔥 Top Matches:")
    for other_name, result in results[:5]:
        print(f"\n{other_name}: {result['score']}% match")
        if result["shared"]:
            print(" Shared:", ", ".join(result["shared"]))
        if result["keywords"] > 0:
            print(" Keyword overlap.")


if __name__ == "__main__":
    main()
