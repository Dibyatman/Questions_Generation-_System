from __future__ import annotations

from fastapi import FastAPI

from question_generation_system.models import QuestionGenerationRequest, QuestionGenerationResponse
from question_generation_system.pipeline import QuestionGenerationPipeline

app = FastAPI(title="Question Generation System", version="1.0.0")
pipeline = QuestionGenerationPipeline()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/generate_questions", response_model=QuestionGenerationResponse)
def generate_questions(request: QuestionGenerationRequest) -> QuestionGenerationResponse:
    return pipeline.run(request)
