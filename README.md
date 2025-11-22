# Food-Friend

🍕 A social food preference matching app powered by local LLM (llama.cpp)

## Features
- Simple username-only login
- Add your food preferences
- AI-powered matching using local LLM
- Find friends with similar tastes
- React frontend + Flask backend

## Prerequisites
- Python 3.8+
- Node.js 16+
- 8GB RAM minimum (for LLM)
- Conda (recommended) or pip

## Installation

### Option 1: Using Conda (Recommended)

1. **Create and activate conda environment:**
```bash
conda env create -f environment.yml
conda activate food-friend
```

2. **Install frontend dependencies:**
```bash
cd frontend
npm install
cd ..
```

### Option 2: Using pip

1. **Create virtual environment (optional but recommended):**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install frontend dependencies:**
```bash
cd frontend
npm install
cd ..
```

### Download LLM Model

Place a GGUF model in the `models/` directory. Recommended:
- **qwen2.5-3b-instruct-q2_k.gguf**
- Download from: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF

```bash
# Create models directory if it doesn't exist
mkdir models

# Download model (example using wget or curl)
# Or download manually from the link above
```

## Running the Application

### Start Backend (Flask API)
```bash
# If using conda:
conda activate food-friend

python api_server.py
```
Backend runs on: http://localhost:5000

### Start Frontend (React) - In a new terminal
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:5173

## Usage
1. Open http://localhost:5173 in your browser
2. Enter your name (no password required)
3. Add your food preferences (e.g., "Pizza", "Sushi", "Tacos")
4. Click "Calculate Matches" to find compatible users
5. AI analyzes preferences and shows top 3 matches with scores
6. Use "Switch User" button to logout and try another user

## How It Works
- User preferences stored in JSON files (`data/users/user_<name>.json`)
- LLM analyzes food compatibility using:
  - Exact dish matching (Jaccard similarity)
  - Cuisine clustering (Korean, Mexican, Italian, etc.)
  - Keyword matching (spicy, fried, grilled, etc.)
- Scores range from 0-100%
- Top 3 matches displayed with detailed breakdown

## Project Structure
```
Food-Friend/
├── api_server.py          # Flask backend API
├── match_engine.py        # Matching algorithm
├── llm_utils.py          # LLM utilities
├── draft_chat_bot.py     # CLI version
├── requirements.txt       # Python dependencies
├── environment.yml        # Conda environment file
├── data/users/           # User JSON files
├── frontend/             # React app
│   ├── src/
│   │   ├── App.jsx       # Main React component
│   │   └── App.css       # Styles
│   └── package.json      # Node dependencies
└── models/               # LLM model files (download separately)
```

## Dependencies

### Python (Backend)
- Flask - Web framework
- flask-cors - CORS support
- llama-cpp-python - LLM inference

### JavaScript (Frontend)
- React 18
- Vite - Build tool

## Sample Users
10 pre-populated users available in `data/users/` for testing:
- Sarah Chen, Marcus Rodriguez, Emily Watson, David Kim, Isabella Rossi
- James Thompson, Priya Patel, Ahmed Hassan, Sophie Dubois, Yuki Tanaka

## Troubleshooting

### LLM Not Loading
- Ensure model file is in `models/` directory
- Check model file name in `config.py`
- Verify you have enough RAM (8GB minimum)

### Backend Connection Issues
- Ensure Flask is running on port 5000
- Check CORS is enabled
- Verify firewall settings

### Frontend Issues
- Clear browser cache
- Check console for errors
- Ensure backend is running first

## Performance Note
Depending on your PC hardware, LLM inference can take a few seconds. GPU acceleration recommended for faster matching. CPU-only inference typically takes 2-5 seconds per match calculation.

## Hackathon Project
This is a hackathon project built in under 1 hour with simplified authentication and streamlined features for rapid demonstration.

## Output - Extended

```
(llamaenv) gsn@gsn-batcomputer:~/Phoenix/AILA/Food-Friend$ python3 chat_bot.py 
Welcome to Food-Friend!
Enter your name: Sowmiya
Loaded existing profile for Sowmiya

llama_context: n_ctx_per_seq (2048) < n_ctx_train (32768) -- the full capacity of the model will not be utilized

Describe your favorite foods or cuisines:
> I like spicy indian food like biriyani

Extracted food choices: ['biriyani']

Saved your preferences!
Finding your top matches...

Top Matches:

Priya Patel: 52% match
  Python score: 34%
  LLM score: 80%
  Reason: The dishes from User A and User B have a strong similarity in terms of spices, flavor profiles, and the presence of several common ingredients. The dishes are primarily from the Indian and biryani cuisines. The strong similarity in flavor and ingredient profiles suggest a strong match.
  Matched cuisines: indian
  Shared dishes: biryani

Jenna: 45% match
  Python score: 35%
  LLM score: 60%
  Reason: The cuisines are very similar, but the dish similarities and ingredient overlap are not strong. The spice levels and cooking styles are not consistent.
  Matched cuisines: indian
  Shared dishes: biryani

Ahmed Hassan: 8% match
  Python score: 0%
  LLM score: 20%
  Reason: User A and User B cuisines, dishes and ingredients are not aligned. No overlap in spices or cooking styles.

Isabella Rossi: 8% match
  Python score: 0%
  LLM score: 20%
  Reason: The cuisines are quite different. User A has Indian cuisine while User B includes Italian, Italian, Italian, Italian, Italian, Italian, Italian, Italian, Italian, Italian cuisine. The dishes are not as similar in flavor. The spice level and cooking style for User A and User B are not strong.

jonathan: 8% match
  Python score: 0%
  LLM score: 20%
  Reason: Cuisine and ingredients are significantly different. No overlap in common ingredients.

Done!
```