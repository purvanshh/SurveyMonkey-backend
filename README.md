# SurveyMonkey Clone – Backend

FastAPI backend for the survey builder (e.g. Answer genius / predict-answer-type).

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload --port 8000
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

## Endpoints

- **GET /health** – Health check
- **POST /api/predict-answer-type** – Predict answer type from question text  
  Body: `{ "question_text": "Enter your name" }`  
  Response: `{ "answer_type": "Single text box" }` (or `null`)

The frontend (Next.js on port 3000) calls this API when Answer genius is enabled. Set `NEXT_PUBLIC_API_URL=http://localhost:8000` in the frontend `.env.local` if the API runs on a different URL.
