from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


class ContentType(str, Enum):
    TEXT = "text"
    EQUATION = "equation"
    DIAGRAM = "diagram"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionType(str, Enum):
    MCQ = "MCQ"
    NUMERIC = "numeric"
    SHORT_ANSWER = "short_answer"
    LONG_ANSWER = "long_answer"


class IngestionInput(BaseModel):
    raw_text: Optional[str] = None
    image_path: Optional[str] = None
    pdf_path: Optional[str] = None


class StructuredContent(BaseModel):
    content_type: ContentType
    normalized_text: str
    formulas: List[str] = Field(default_factory=list)
    diagram_descriptions: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class ConceptTag(BaseModel):
    concept: str
    concept_type: str
    weight: float = 1.0


class ConceptExtractionOutput(BaseModel):
    key_topics: List[str] = Field(default_factory=list)
    formulas: List[str] = Field(default_factory=list)
    concepts: List[ConceptTag] = Field(default_factory=list)


class DifficultyDistribution(BaseModel):
    easy: int = 0
    medium: int = 0
    hard: int = 0

    def total(self) -> int:
        return self.easy + self.medium + self.hard


class QuestionGenerationRequest(BaseModel):
    subject: str
    chapter: str = "Unknown Chapter"
    chapter_content: str
    total_questions: int
    difficulty_distribution: DifficultyDistribution
    numeric_questions: int = 0
    diagram_required: bool = False
    question_types: List[QuestionType]
    example_questions: Optional[List[str]] = None
    model_to_use: str = "mock-llm"

    @model_validator(mode="after")
    def validate_distribution(self) -> "QuestionGenerationRequest":
        if self.difficulty_distribution.total() != self.total_questions:
            raise ValueError("difficulty_distribution must sum to total_questions")
        if self.numeric_questions > self.total_questions:
            raise ValueError("numeric_questions cannot exceed total_questions")
        return self


class QuestionPlanItem(BaseModel):
    question_number: int
    difficulty: Difficulty
    question_type: QuestionType
    concept: str
    diagram_required: bool = False


class QuestionPlan(BaseModel):
    items: List[QuestionPlanItem]


class GeneratedQuestion(BaseModel):
    question_id: str
    subject: str
    chapter: str
    concept: str
    difficulty: Difficulty
    question_type: QuestionType
    question_text: str
    options: List[str] = Field(default_factory=list)
    correct_answer: str
    explanation: str
    marks: int
    diagram_required: bool = False
    diagram_prompt: str = ""


class QuestionGenerationResponse(BaseModel):
    questions: List[GeneratedQuestion]
    metadata: dict = Field(default_factory=dict)
