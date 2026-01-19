# llm_full_matcher.py
import json
import re

FULL_MATCH_PROMPT = """Analyze food compatibility between two people.

User A likes: {foods_a}
User B likes: {foods_b}

Consider cuisine types, flavor profiles, and specific dishes.

Rate compatibility 0-100:
- 0-20: Very different tastes
- 20-40: Some differences
- 40-60: Moderate match
- 60-80: Good match
- 80-100: Excellent match

Respond with ONLY this JSON (no other text):
{{"score": 75, "reason": "Both enjoy Italian and Asian cuisines with pasta overlap"}}
"""

def llm_full_match(llm, userA, userB):
    foods_a = ", ".join(userA.get("foodChoices", []))
    foods_b = ", ".join(userB.get("foodChoices", []))
    
    if not foods_a or not foods_b:
        return {"score": 0, "reason": "Missing food preferences"}
    
    prompt = FULL_MATCH_PROMPT.format(foods_a=foods_a, foods_b=foods_b)

    try:
        out = llm(prompt, max_tokens=120, temperature=0.3, stop=["}", "\n\n"])
        raw = out["choices"][0]["text"].strip()
        
        # Add closing brace if missing
        if raw and not raw.endswith("}"):
            raw += "}"
        
        print(f"🤖 LLM raw: {raw[:80]}...")  # Debug output
        
        # Strategy 1: Look for complete JSON with both fields
        match = re.search(r'\{\s*"score"\s*:\s*(\d+)\s*,\s*"reason"\s*:\s*"([^"]*)"', raw)
        if match:
            score = int(match.group(1))
            reason = match.group(2)
            score = max(0, min(100, score))
            print(f"✅ Parsed: {score}% - {reason[:40]}")
            return {"score": score, "reason": reason}
        
        # Strategy 2: Try full JSON parse
        json_match = re.search(r'\{[^}]*\}', raw, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                if "score" in data:
                    score = int(data.get("score", 50))
                    score = max(0, min(100, score))
                    reason = data.get("reason", "Compatible food preferences")
                    print(f"✅ JSON parsed: {score}%")
                    return {"score": score, "reason": reason}
            except:
                pass
        
        # Strategy 3: Extract score from any number found
        score_match = re.search(r'(?:score|compatibility|match)[:\s]*(\d+)', raw, re.IGNORECASE)
        if score_match:
            score = int(score_match.group(1))
            score = max(0, min(100, score))
            # Try to find any descriptive text
            reason_match = re.search(r'(?:reason|because|analysis)[:\s]*["\']?([^"\'\n]{10,100})', raw, re.IGNORECASE)
            reason = reason_match.group(1).strip() if reason_match else "Based on food preferences"
            print(f"⚠️ Fuzzy parse: {score}%")
            return {"score": score, "reason": reason}
        
        # Strategy 4: Fallback - analyze overlap manually
        print(f"⚠️ All parsing failed, using overlap analysis")
        foods_a_set = set(f.lower().strip() for f in foods_a.split(","))
        foods_b_set = set(f.lower().strip() for f in foods_b.split(","))
        overlap = foods_a_set & foods_b_set
        
        if overlap:
            score = min(80, 40 + len(overlap) * 10)
            reason = f"Share interest in {', '.join(list(overlap)[:3])}"
        else:
            score = 30
            reason = "Different food preferences but may discover new tastes"
        
        return {"score": score, "reason": reason}
        
    except Exception as e:
        print(f"❌ LLM error: {e}")
        # Last resort: simple overlap
        try:
            foods_a_set = set(f.lower().strip() for f in foods_a.split(","))
            foods_b_set = set(f.lower().strip() for f in foods_b.split(","))
            overlap = foods_a_set & foods_b_set
            score = min(70, 30 + len(overlap) * 15)
            return {"score": score, "reason": "Automatic compatibility analysis"}
        except:
            return {"score": 50, "reason": "Analysis completed"}
