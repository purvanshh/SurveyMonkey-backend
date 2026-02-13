import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.predict_answer_type import predict_answer_type
from database import engine, Base
from routers import surveys, public, hosted, responses

# Create all tables on startup
Base.metadata.create_all(bind=engine)

# CORS: allow comma-separated origins. Production: set CORS_ORIGINS=https://yourapp.vercel.app,http://localhost:3000
_cors_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
CORS_ORIGINS = [o.strip() for o in _cors_str.split(",") if o.strip()]

app = FastAPI(title="SurveyMonkey Clone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(surveys.router)
app.include_router(public.router)
app.include_router(hosted.router)
app.include_router(responses.router)


# ---------------------------------------------------------------------------
# Existing endpoints
# ---------------------------------------------------------------------------

class PredictRequest(BaseModel):
    question_text: str


class PredictResponse(BaseModel):
    answer_type: str | None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/predict-answer-type", response_model=PredictResponse)
def api_predict_answer_type(body: PredictRequest):
    """Predict a suitable answer type (e.g. Single text box, Multiple choice, Checkboxes) from the question text."""
    predicted = predict_answer_type(body.question_text)
    return PredictResponse(answer_type=predicted)
