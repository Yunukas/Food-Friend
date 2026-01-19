# api_server.py
"""
Flask API server for Food-Friend
Connects the React frontend with the LLM-based matching logic
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
APP_NAME = os.getenv('APP_NAME', 'Food Friend')
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')

from llm_utils_updated import load_llm, extract_food_choices
from llm_hybrid_matcher import llm_hybrid_match

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

DATA_DIR = "data/users"
os.makedirs(DATA_DIR, exist_ok=True)

# Load LLM once at startup
print("🔄 Loading LLM model...")
try:
    llm = load_llm()
    print("✅ LLM loaded successfully!")
    print(f"   Model ready for inference")
except Exception as e:
    print(f"❌ Failed to load LLM: {e}")
    print("   Server will start but matching will fail")
    llm = None


def user_file_by_name(name):
    """Get user file path by name"""
    safe = name.replace(" ", "_").lower()
    return os.path.join(DATA_DIR, f"user_{safe}.json")


def load_user_by_name(name):
    """Load user data by name"""
    path = user_file_by_name(name)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def save_user_json(data):
    """Save user JSON file"""
    with open(user_file_by_name(data["name"]), "w") as f:
        json.dump(data, f, indent=2)


def load_all_users(exclude=None):
    """Load all users except the specified one"""
    users = []
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".json"):
            continue
        
        path = os.path.join(DATA_DIR, fname)
        try:
            with open(path) as f:
                data = json.load(f)
            
            if "name" not in data:
                continue
            
            if exclude and data["name"].lower() == exclude.lower():
                continue
            
            data.setdefault("foodChoices", [])
            users.append(data)
        except:
            continue
    
    return users


@app.route('/api/login', methods=['POST'])
def login():
    """Login or create user"""
    data = request.json
    name = data.get('name', '').strip()
    
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    user = load_user_by_name(name)
    
    if user:
        return jsonify({
            "success": True,
            "user": user,
            "isNew": False
        })
    else:
        # Create new user
        new_user = {
            "name": name,
            "foodChoices": [],
            "createdAt": datetime.now().isoformat(),
            "lastUpdated": datetime.now().isoformat()
        }
        save_user_json(new_user)
        
        return jsonify({
            "success": True,
            "user": new_user,
            "isNew": True
        })


@app.route('/api/update-foods', methods=['POST'])
def update_foods():
    """Update user's food choices"""
    data = request.json
    name = data.get('name', '').strip()
    food_choices = data.get('foodChoices', [])
    
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    user = load_user_by_name(name)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user['foodChoices'] = food_choices
    user['lastUpdated'] = datetime.now().isoformat()
    save_user_json(user)
    
    return jsonify({
        "success": True,
        "user": user
    })


@app.route('/api/extract-foods', methods=['POST'])
def extract_foods():
    """Extract food choices from natural language description using LLM"""
    data = request.json
    description = data.get('description', '').strip()
    
    if not description:
        return jsonify({"error": "Description is required"}), 400
    
    try:
        choices = extract_food_choices(llm, description)
        return jsonify({
            "success": True,
            "foodChoices": choices if isinstance(choices, list) else []
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/calculate-matches', methods=['POST'])
def calculate_matches():
    """Calculate compatibility matches for a user"""
    data = request.json
    name = data.get('name', '').strip()
    
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    user = load_user_by_name(name)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if not user.get('foodChoices'):
        return jsonify({"error": "No food preferences set"}), 400
    
    # Load other users
    others = load_all_users(exclude=name)
    
    if not others:
        return jsonify({
            "success": True,
            "matches": []
        })
    
    # Calculate scores using hybrid matcher (Python + LLM)
    # Performance optimization: Only use expensive LLM scoring on top Python matches
    
    # Check if LLM is loaded
    if llm is None:
        return jsonify({"error": "LLM not loaded. Please restart the server."}), 500
    
    results = []
    
    # First pass: Quick Python-only scoring
    from match_engine import score_pair
    quick_scores = []
    for other in others:
        py_score = score_pair(user, other)
        quick_scores.append((other, py_score))
    
    # Sort and take top 5 candidates for full LLM analysis
    quick_scores.sort(key=lambda x: x[1]["score"], reverse=True)
    top_candidates = quick_scores[:5]
    
    # Second pass: Full hybrid scoring on top candidates only
    print(f"🔍 Analyzing top {len(top_candidates)} candidates with LLM...")
    for other, py_result in top_candidates:
        scoreinfo = llm_hybrid_match(llm, user, other)
        results.append({
            "name": other["name"],
            "score": scoreinfo["final_score"],
            "sharedFoods": scoreinfo.get("shared_exact", []),
            "matchedCuisines": scoreinfo.get("matched_cuisines", []),
            "keywordHits": scoreinfo.get("keyword_hits", []),
            "llmReason": scoreinfo.get("reason", ""),
            "pythonScore": scoreinfo.get("python_score", 0),
            "llmScore": scoreinfo.get("llm_score", 0)
        })
    print(f"✅ Completed analysis")
    
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return jsonify({
        "success": True,
        "matches": results[:3]  # Return top 3 matches
    })


@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = load_all_users()
    return jsonify({
        "success": True,
        "users": users
    })


if __name__ == '__main__':
    print(f"\n🍕 {APP_NAME} API Server v{APP_VERSION}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
