# llm_full_matcher.py
import json

FULL_MATCH_PROMPT = """
You are Food-Friend, an offline food compatibility expert.

Consider:
- cuisines
- spice levels
- cooking style
- dish similarities
- ingredient overlap
- flavor profile

Scoring Rubric:
0–20  = very low similarity
20–40 = weak match
40–60 = moderate
60–80 = strong
80–100 = very strong

Be strict and realistic. Do NOT repeat the same score for all users.

Output ONLY:
{
  "score": <integer>,
  "reason": "<string>"
}
"""

def llm_full_match(llm, userA, userB):
    prompt = f"""
{FULL_MATCH_PROMPT}

User A foods:
{json.dumps(userA.get("foodChoices", []), indent=2)}

User B foods:
{json.dumps(userB.get("foodChoices", []), indent=2)}

JSON OUTPUT:
"""

    out = llm(prompt, max_tokens=80, temperature=0.4)
    raw = out["choices"][0]["text"].strip()

    import re
    match = re.search(r"\{(.|\n)*\}", raw)
    if not match:
        return {"score": 0, "reason": "Unable to determine."}

    try:
        data = json.loads(match.group(0))
        score = int(data.get("score", 0))
        score = max(0, min(100, score))
        return {"score": score, "reason": data.get("reason", "")}
    except:
        return {"score": 0, "reason": "Invalid JSON."}
