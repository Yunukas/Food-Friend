#!/usr/bin/env python3
"""
Food Friend - Offline Local LLM App (llama.cpp + GGUF)

Features:
- Runs entirely offline using llama.cpp + local GGUF model
- Collects food preferences from multiple people
- Uses LLM to extract structured preference profiles (JSON)
- Aggregates group preferences with a Python matching engine
- Asks LLM to explain the final group recommendation in natural language
"""

import json
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from llama_cpp import Llama
from config import (
    MODEL_PATH,
    DEFAULT_CONTEXT_SIZE,
    DEFAULT_GPU_LAYERS,
    DEFAULT_PARAMS,
    check_model_exists,
    print_section,
)

# ==================== DATA MODEL ====================

@dataclass
class FoodProfile:
    name: str
    cuisines: List[str]
    likes: List[str]
    dislikes: List[str]
    avoid: List[str]
    diet: Optional[str]
    spice_tolerance: Optional[str]
    budget: Optional[str]
    notes: Optional[str]

    @staticmethod
    def empty(name: str, notes: str = "") -> "FoodProfile":
        return FoodProfile(
            name=name,
            cuisines=[],
            likes=[],
            dislikes=[],
            avoid=[],
            diet=None,
            spice_tolerance=None,
            budget=None,
            notes=notes or None,
        )

# In-memory "DB"
GROUP_PROFILES: List[FoodProfile] = []


# ==================== LLM SETUP ====================

def create_llm() -> Llama:
    check_model_exists()
    print_section("Loading local model (Food Friend)")
    llm = Llama(
        model_path=str(MODEL_PATH),
        n_ctx=DEFAULT_CONTEXT_SIZE,
        n_gpu_layers=DEFAULT_GPU_LAYERS,
        verbose=False,
    )
    print(f"✅ Model loaded from: {MODEL_PATH}")
    print(f"Context size: {llm.n_ctx()} tokens")
    print(f"Vocab size: {llm.n_vocab()} tokens\n")
    return llm


# ==================== JSON HELPERS ====================

def extract_json_block(text: str) -> Optional[str]:
    """Extract the first {...} block from the text."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    candidate = text[start : end + 1]
    # Strip code fences if any
    candidate = candidate.replace("```json", "").replace("```", "").strip()
    return candidate


def parse_json_safely(text: str) -> Optional[Dict[str, Any]]:
    """Best-effort JSON parser for model output."""
    block = extract_json_block(text)
    if block is None:
        return None

    # Light cleanup: fix single quotes, remove trailing commas
    cleaned = block

    # Replace single quotes with double quotes (only if not already clearly JSON)
    if "'" in cleaned and '"' not in cleaned:
        cleaned = cleaned.replace("'", '"')

    # Remove trailing commas before } or ]
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None


# ==================== TOOL: PREFERENCE EXTRACTION ====================

PREFERENCE_EXTRACTION_SYSTEM = (
    "You are Food Friend, an assistant that extracts structured food preferences.\n"
    "You ONLY output a single JSON object matching this schema:\n"
    "{\n"
    '  "name": "<string>",\n'
    '  "cuisines": ["<string>", ...],\n'
    '  "likes": ["<string>", ...],\n'
    '  "dislikes": ["<string>", ...],\n'
    '  "avoid": ["<string>", ...],\n'
    '  "diet": "<string or null>",\n'
    '  "spice_tolerance": "<string or null>",\n'
    '  "budget": "<string or null>",\n'
    '  "notes": "<string or null>"\n'
    "}\n"
    "If some fields are not mentioned, use empty lists [] or null.\n"
    "Do not output any explanation, only JSON.\n"
)

def llm_extract_preferences(llm: Llama, name: str, description: str) -> FoodProfile:
    prompt = (
        PREFERENCE_EXTRACTION_SYSTEM
        + "\nUser:\n"
        f"Name: {name}\n"
        f"Description: {description}\n\n"
        "JSON:\n"
    )

    output = llm(
        prompt,
        max_tokens=256,
        temperature=0.2,
        top_p=DEFAULT_PARAMS["top_p"],
        top_k=DEFAULT_PARAMS["top_k"],
        repeat_penalty=DEFAULT_PARAMS["repeat_penalty"],
    )

    text = output["choices"][0]["text"]
    data = parse_json_safely(text)

    if data is None:
        # Fallback: minimal profile with notes
        return FoodProfile.empty(name=name, notes=description)

    def get_list(key: str) -> List[str]:
        val = data.get(key, [])
        if isinstance(val, list):
            return [str(x).strip() for x in val if str(x).strip()]
        if isinstance(val, str) and val.strip():
            return [val.strip()]
        return []

    def get_str_or_none(key: str) -> Optional[str]:
        val = data.get(key)
        if val is None:
            return None
        s = str(val).strip()
        return s or None

    profile = FoodProfile(
        name=data.get("name") or name,
        cuisines=get_list("cuisines"),
        likes=get_list("likes"),
        dislikes=get_list("dislikes"),
        avoid=get_list("avoid"),
        diet=get_str_or_none("diet"),
        spice_tolerance=get_str_or_none("spice_tolerance"),
        budget=get_str_or_none("budget"),
        notes=get_str_or_none("notes"),
    )
    return profile


# ==================== TOOL: GROUP RECOMMENDATION ENGINE ====================

def compute_group_stats(profiles: List[FoodProfile]) -> Dict[str, Any]:
    """
    Simple heuristic-based group recommender.

    Returns a dict with:
    - cuisines_scores: {cuisine: score}
    - common_cuisines: [cuisine, ...]
    - conflicts: [text, ...]
    """
    cuisine_counts = {}
    cuisine_dislikes = {}
    conflicts = []

    if not profiles:
        return {
            "cuisines_scores": {},
            "common_cuisines": [],
            "conflicts": ["No profiles provided."],
        }

    # Count likes per cuisine, track dislikes
    for p in profiles:
        for c in p.cuisines:
            c_norm = c.strip().lower()
            if not c_norm:
                continue
            cuisine_counts[c_norm] = cuisine_counts.get(c_norm, 0) + 1

        for d in p.dislikes + p.avoid:
            d_norm = d.strip().lower()
            if not d_norm:
                continue
            cuisine_dislikes.setdefault(d_norm, []).append(p.name)

    # Basic conflicts: if a cuisine is liked by some and appears in dislikes
    for cuisine, count in cuisine_counts.items():
        if cuisine in cuisine_dislikes:
            conflicts.append(
                f"{cuisine.title()} is liked by {count} people but disliked/avoided by: "
                + ", ".join(cuisine_dislikes[cuisine])
            )

    # Common cuisines: liked by everyone
    num_people = len(profiles)
    common = [c for c, cnt in cuisine_counts.items() if cnt == num_people]

    # Sort cuisines by score desc
    sorted_scores = dict(
        sorted(cuisine_counts.items(), key=lambda kv: kv[1], reverse=True)
    )

    return {
        "cuisines_scores": sorted_scores,
        "common_cuisines": common,
        "conflicts": conflicts,
    }


def llm_explain_recommendation(
    llm: Llama,
    profiles: List[FoodProfile],
    stats: Dict[str, Any],
) -> str:
    """Ask LLM to produce a friendly explanation for the group."""

    profiles_json = json.dumps([asdict(p) for p in profiles], indent=2)
    stats_json = json.dumps(stats, indent=2)

    prompt = (
        "You are Food Friend, helping a group decide what to eat.\n"
        "You are given structured food preference profiles and some computed stats.\n"
        "Your job: explain good options for the group in a friendly, concise way.\n\n"
        "Constraints:\n"
        "- Mention 2–4 cuisine directions that work well.\n"
        "- Briefly note any important conflicts or constraints.\n"
        "- Keep it under ~200 words.\n\n"
        "=== PROFILES ===\n"
        f"{profiles_json}\n\n"
        "=== STATS ===\n"
        f"{stats_json}\n\n"
        "Now write your recommendation:\n"
    )

    output = llm(
        prompt,
        max_tokens=256,
        temperature=0.6,
        top_p=DEFAULT_PARAMS["top_p"],
        top_k=DEFAULT_PARAMS["top_k"],
        repeat_penalty=DEFAULT_PARAMS["repeat_penalty"],
    )

    return output["choices"][0]["text"].strip()


# ==================== UI HELPERS ====================

def print_main_menu():
    print_section("Food Friend - Group Food Preference Assistant")
    print("Choose an option:")
    print("  1) Add a person's preferences")
    print("  2) Show current group profiles")
    print("  3) Get group recommendations")
    print("  4) Clear all profiles")
    print("  0) Exit")
    print()


def pretty_print_profile(p: FoodProfile, idx: int):
    print(f"[{idx}] {p.name}")
    if p.cuisines:
        print(f"   Cuisines: {', '.join(p.cuisines)}")
    if p.likes:
        print(f"   Likes: {', '.join(p.likes)}")
    if p.dislikes:
        print(f"   Dislikes: {', '.join(p.dislikes)}")
    if p.avoid:
        print(f"   Avoid: {', '.join(p.avoid)}")
    if p.diet:
        print(f"   Diet: {p.diet}")
    if p.spice_tolerance:
        print(f"   Spice tolerance: {p.spice_tolerance}")
    if p.budget:
        print(f"   Budget: {p.budget}")
    if p.notes:
        print(f"   Notes: {p.notes}")
    print()


# ==================== FLOWS ====================

def add_person_flow(llm: Llama):
    print_section("Add Person")
    name = input("Person's name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    print("\nDescribe their food preferences in a few sentences.")
    print("You can mention cuisines, favorite dishes, dietary restrictions,")
    print("foods they dislike, spice tolerance, budget, etc.\n")
    desc = input(f"{name}'s preferences: ").strip()
    if not desc:
        print("No description provided, skipping.")
        return

    print("\nExtracting structured preferences with the LLM...")
    profile = llm_extract_preferences(llm, name, desc)

    print("\nHere is what I understood:")
    pretty_print_profile(profile, idx=len(GROUP_PROFILES) + 1)

    confirm = input("Add this profile to the group? [y/N]: ").strip().lower()
    if confirm == "y":
        GROUP_PROFILES.append(profile)
        print(f"✅ Added {profile.name} to the group.\n")
    else:
        print("Profile discarded.\n")


def show_group_profiles():
    print_section("Current Group Profiles")
    if not GROUP_PROFILES:
        print("No profiles yet. Add someone first.\n")
        return
    for i, p in enumerate(GROUP_PROFILES, start=1):
        pretty_print_profile(p, i)


def recommend_flow(llm: Llama):
    print_section("Group Recommendation")
    if not GROUP_PROFILES:
        print("No profiles available. Add at least one person first.\n")
        return

    stats = compute_group_stats(GROUP_PROFILES)

    print("Computed stats (for debugging / transparency):")
    print(json.dumps(stats, indent=2))
    print()

    explanation = llm_explain_recommendation(llm, GROUP_PROFILES, stats)

    print("🍽️ Food Friend Recommendation:\n")
    print(explanation)
    print()


def clear_profiles_flow():
    global GROUP_PROFILES
    GROUP_PROFILES = []
    print("\n🧹 Cleared all profiles.\n")


# ==================== MAIN ====================

def main():
    llm = create_llm()

    while True:
        print_main_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_person_flow(llm)
        elif choice == "2":
            show_group_profiles()
        elif choice == "3":
            recommend_flow(llm)
        elif choice == "4":
            clear_profiles_flow()
        elif choice == "0":
            print("\nGoodbye from Food Friend! 🍽️\n")
            break
        else:
            print("Invalid choice. Please select 0–4.\n")


if __name__ == "__main__":
    main()
