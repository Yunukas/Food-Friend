# match_engine.py

KEYWORDS = [
    "spicy", "sweet", "sour",
    "fried", "grilled", "roasted",
    "biryani", "curry", "noodles", "pasta", "tacos",
    "sushi", "bbq", "pizza"
]

def keyword_overlap_score(list1, list2):
    score = 0
    for item1 in list1:
        for item2 in list2:
            # Simple bag-of-words overlap
            for kw in KEYWORDS:
                if kw in item1.lower() and kw in item2.lower():
                    score += 5
    return min(score, 20)

def jaccard_similarity(list1, list2):
    set1 = set(item.lower() for item in list1)
    set2 = set(item.lower() for item in list2)
    if not set1 or not set2:
        return 0
    return len(set1 & set2) / len(set1 | set2)

def score_pair(a: dict, b: dict) -> dict:
    foods1 = a.get("foodChoices", [])
    foods2 = b.get("foodChoices", [])

    jac = jaccard_similarity(foods1, foods2)
    jac_score = int(jac * 70)   # max 70%

    kw_score = keyword_overlap_score(foods1, foods2)  # max 20%

    final_score = min(jac_score + kw_score, 100)

    return {
        "score": final_score,
        "shared": list(set(foods1) & set(foods2)),
        "keywords": kw_score
    }
