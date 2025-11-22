# llm_utils.py
import re
from llama_cpp import Llama
from config import (
    MODEL_PATH,
    DEFAULT_CONTEXT_SIZE,
    DEFAULT_GPU_LAYERS,
    DEFAULT_PARAMS,
    check_model_exists
)

EXTRACTION_PROMPT = """
You are Food-Friend, an assistant that extracts food preferences.

Your task: From the user's description, extract a list of foods/cuisines they like.

Rules:
- ONLY extract items the user says they like.
- If the user mentions multiple items separated by commas, split them.
- If the user lists items with words like "and", "or", etc., split them too.
- If unsure, output 1–3 reasonable food-related items from the text.
- Do NOT add explanations.
- Do NOT include items they did NOT say they like.

Output format (IMPORTANT):
Foods: item1, item2, item3
"""

def load_llm():
    check_model_exists()
    return Llama(
        model_path=str(MODEL_PATH),
        n_ctx=DEFAULT_CONTEXT_SIZE,
        n_gpu_layers=DEFAULT_GPU_LAYERS,
        verbose=False
    )

def extract_food_choices(llm, text: str):
    """
    Extracts and splits food choices using comma and simple delimiter logic.
    With fallback for when the model does not follow the prompt.
    """

    prompt = EXTRACTION_PROMPT + f"\nUser: {text}\n\nExtract:\n"

    output = llm(
        prompt,
        max_tokens=128,
        temperature=0.4,
        top_p=DEFAULT_PARAMS["top_p"],
        top_k=DEFAULT_PARAMS["top_k"],
        repeat_penalty=DEFAULT_PARAMS["repeat_penalty"]
    )

    raw = output["choices"][0]["text"].strip()

    # ----------------------------------------
    # 1) Look for "Foods:" line
    # ----------------------------------------
    match = re.search(r"Foods:(.*)", raw, re.IGNORECASE)

    if match:
        items = match.group(1).strip()
    else:
        # ----------------------------------------
        # 2) FALLBACK extractor for Qwen:
        # ----------------------------------------
        # Look for any food-like words
        fallback_items = re.findall(
            r"\b(?:biryani|curry|rice|dosa|tacos?|fries|pizza|pasta|bbq|indian|thai|mexican|chicken|curry|noodles|spicy)\b",
            text,
            flags=re.IGNORECASE
        )
        return list(set([f.lower() for f in fallback_items]))

    # ----------------------------------------
    # 3) Clean + split items
    # ----------------------------------------
    items = re.sub(r"\band\b|\bor\b", ",", items, flags=re.IGNORECASE)
    parts = [p.strip() for p in items.split(",") if p.strip()]

    # ----------------------------------------
    # 4) FINAL FALLBACK if empty after split
    # ----------------------------------------
    if not parts:
        fallback_items = re.findall(
            r"\b(?:biryani|curry|rice|dosa|tacos?|fries|pizza|pasta|bbq|indian|thai|mexican|chicken|curry|noodles|spicy)\b",
            text,
            flags=re.IGNORECASE
        )
        return list(set([f.lower() for f in fallback_items]))

    return parts

