# match_engine.py

# --------------------------------------------------------
# Cuisine keyword dictionary
# --------------------------------------------------------
CUISINE_KEYWORDS = {
    "mexican": [
        "tacos", "burrito", "enchilada", "queso", "chimichanga",
        "nachos", "barbacoa", "asada", "elote", "churro"
    ],
    "indian": [
        "biryani", "curry", "masala", "tandoori", "dal",
        "naan", "paneer", "vindaloo", "spicy"
    ],
    "korean": [
        "kimchi", "bibimbap", "bulgogi", "jajangmyeon",
        "tteokbokki", "gochujang", "korean bbq", "galbi",
        "japchae", "fried chicken", "pancake"
    ],
    "japanese": [
        "sushi", "ramen", "tempura", "udon",
        "donburi", "teriyaki", "miso"
    ],
    "italian": [
        "pasta", "pizza", "lasagna", "ravioli",
        "gnocchi", "risotto", "tiramisu"
    ],
    "thai": [
        "pad thai", "green curry", "red curry", "tom yum",
        "massaman", "papaya salad"
    ],
    "chinese": [
        "noodles", "kung pao", "dumplings", "mapo tofu",
        "fried rice", "hotpot"
    ],
    "vietnamese": [
        "vietnamese", "pho", "pho bo", "pho ga", "bun cha", "bun bo hue",
        "banh mi", "banh xeo", "com tam", "hu tieu", "goi cuon", "cha gio",
        "nem", "bun rieu", "mi quang", "ca phe sua da", "spring roll"
    ],
    "taiwanese": [
        "taiwanese", "beef noodle", "beef noodle soup", "lu rou fan",
        "braised pork rice", "xiao long bao", "stinky tofu", "bubble tea",
        "boba", "gua bao", "three cup chicken", "taiwanese breakfast",
        "salt and pepper chicken", "taiwanese street food", "night market"
    ]
}

# --------------------------------------------------------
# General cooking / taste keywords
# --------------------------------------------------------
GENERAL_KEYWORDS = [
    "spicy", "sweet", "savory", "crispy", "fried",
    "grilled", "bbq", "noodles", "soup", "rice",
    "seafood", "chicken", "beef", "pork",
    "vegan", "vegetarian"
]

# --------------------------------------------------------
# NORMALIZATION: Expand cuisine terms (CRITICAL FIX)
# --------------------------------------------------------
def normalize_food_list(food_list):
    """
    Converts items like "Korean food" or "Mexican cuisine"
    into full cuisine keyword sets.
    """
    normalized = []

    for item in food_list:
        s = item.lower()

        # Cuisine → expand keywords
        for cuisine, words in CUISINE_KEYWORDS.items():
            if cuisine in s:     # e.g., "korean food"
                normalized.extend(words)
                break
        else:
            # keep the dish as-is
            normalized.append(s)

    return normalized


# --------------------------------------------------------
# Cuisine similarity (based on clusters)
# --------------------------------------------------------
def cuisine_similarity(foods1, foods2):
    f1 = " ".join(foods1)
    f2 = " ".join(foods2)

    score = 0
    matched_cuisines = []

    for cuisine, words in CUISINE_KEYWORDS.items():
        in1 = any(w in f1 for w in words)
        in2 = any(w in f2 for w in words)

        if in1 and in2:
            score += 30
            matched_cuisines.append(cuisine)

    return min(score, 60), matched_cuisines


# --------------------------------------------------------
# General keyword overlap (weak signal)
# --------------------------------------------------------
def keyword_similarity(foods1, foods2):
    f1 = " ".join(foods1)
    f2 = " ".join(foods2)

    score = 0
    hits = []

    for kw in GENERAL_KEYWORDS:
        if kw in f1 and kw in f2:
            score += 5
            hits.append(kw)

    return min(score, 20), hits


# --------------------------------------------------------
# Jaccard similarity (exact dish overlap)
# --------------------------------------------------------
def jaccard_similarity(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    if not set1 or not set2:
        return 0, []

    intersection = list(set1 & set2)
    score = len(intersection) / len(set1 | set2)

    return score, intersection


# --------------------------------------------------------
# FINAL COMPATIBILITY SCORING
# --------------------------------------------------------
def score_pair(user_a, user_b):
    # Normalize (handle “Korean food”, “Mexican cuisine”, etc.)
    foods1 = normalize_food_list(user_a.get("foodChoices", []))
    foods2 = normalize_food_list(user_b.get("foodChoices", []))

    # 1. Exact item overlap
    jac_value, jac_matches = jaccard_similarity(foods1, foods2)
    jac_score = int(jac_value * 40)  # up to 40 pts

    # 2. Cuisine cluster match
    cuisine_score, cuisines_matched = cuisine_similarity(foods1, foods2)

    # 3. General keyword similarity
    kw_score, kw_hits = keyword_similarity(foods1, foods2)

    final_score = min(jac_score + cuisine_score + kw_score, 100)

    return {
        "score": final_score,
        "shared_exact": jac_matches,
        "matched_cuisines": cuisines_matched,
        "keyword_hits": kw_hits
    }
