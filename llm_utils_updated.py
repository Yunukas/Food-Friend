# llm_utils.py
import re
import os
from llama_cpp import Llama
from dotenv import load_dotenv
from config import (
    MODEL_PATH,
    DEFAULT_CONTEXT_SIZE,
    DEFAULT_GPU_LAYERS,
    DEFAULT_PARAMS,
    check_model_exists
)

# Load environment variables
load_dotenv()
APP_NAME = os.getenv('APP_NAME', 'Food Friend')

EXTRACTION_PROMPT = f"""
You are {APP_NAME}, an assistant that extracts food preferences.

Return ONLY items the user says they like.

Output format:
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
    prompt = EXTRACTION_PROMPT + f"\nUser: {text}\n\nExtract:\n"

    output = llm(
        prompt,
        max_tokens=80,
        temperature=0.3,
        top_p=DEFAULT_PARAMS["top_p"],
        top_k=DEFAULT_PARAMS["top_k"],
        repeat_penalty=DEFAULT_PARAMS["repeat_penalty"]
    )

    raw = output["choices"][0]["text"].strip()

    match = re.search(r"Foods:(.*)", raw, re.IGNORECASE)
    if match:
        items = match.group(1).strip()
    else:
        fallback = re.findall(
            r"\b(biryani|biriyani|rice|noodles|pizza|korean|indian|mexican|thai|pasta|bbq|spicy)\b",
            text, re.IGNORECASE
        )
        return list({x.lower() for x in fallback})

    parts = [x.strip() for x in items.replace("and", ",").split(",") if x.strip()]
    return parts
