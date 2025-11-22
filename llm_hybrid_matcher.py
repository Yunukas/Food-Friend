# llm_hybrid_matcher.py
import json
from llm_full_matcher import llm_full_match
from match_engine import score_pair

def llm_hybrid_match(llm, userA, userB):
    python_result = score_pair(userA, userB)
    python_score = python_result["score"]

    llm_result = llm_full_match(llm, userA, userB)
    llm_score = llm_result["score"]

    final_score = int(0.6 * python_score + 0.4 * llm_score)
    final_score = max(0, min(100, final_score))

    return {
        "final_score": final_score,
        "python_score": python_score,
        "llm_score": llm_score,
        "reason": llm_result["reason"],
        "matched_cuisines": python_result["matched_cuisines"],
        "shared_exact": python_result["shared_exact"],
        "keyword_hits": python_result["keyword_hits"],
    }
