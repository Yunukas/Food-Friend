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

## Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download LLM Model
Place a GGUF model in the `models/` directory. Recommended:
- **qwen2.5-3b-instruct-q2_k.gguf**
- Download from: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
```

## Running the Application

### Start Backend (Flask API)
```bash
python api_server.py
```
Backend runs on: http://localhost:5000

### Start Frontend (React)
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:5173

## Usage
1. Open http://localhost:5173 in your browser
2. Enter your name (no password required)
3. Add your food preferences
4. Click "Calculate Matches" to find compatible users
5. AI analyzes preferences and shows match scores

## How It Works
- User preferences stored in JSON files (`data/users/`)
- LLM analyzes food compatibility using:
  - Exact dish matching (Jaccard similarity)
  - Cuisine clustering (Korean, Mexican, Italian, etc.)
  - Keyword matching (spicy, fried, grilled, etc.)
- Scores range from 0-100%

## Project Structure
```
Food-Friend/
├── api_server.py          # Flask backend API
├── match_engine.py        # Matching algorithm
├── llm_utils.py          # LLM utilities
├── draft_chat_bot.py     # CLI version
├── data/users/           # User JSON files
├── frontend/             # React app
└── models/               # LLM model files
```

## Sample Users
10 pre-populated users available in `data/users/` for testing

## Note
Depending on your PC hardware, LLM inference can take a few seconds. GPU acceleration recommended for faster matching.