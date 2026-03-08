from __future__ import annotations

from typing import Protocol

from question_generation_system.models import (
    Difficulty,
    GeneratedQuestion,
    QuestionGenerationRequest,
    QuestionPlan,
    QuestionType,
)


class LLMAdapter(Protocol):
    def generate(self, prompt: str, model: str) -> str:
        ...


class MockLLMAdapter:
    """A deterministic adapter used for local/offline development."""

    def generate(self, prompt: str, model: str) -> str:
        return f"[{model}] {prompt}"


class QuestionGenerationModule:
    def __init__(self, llm_adapter: LLMAdapter | None = None) -> None:
        self.llm_adapter = llm_adapter or MockLLMAdapter()

    def generate(
        self,
        request: QuestionGenerationRequest,
        plan: QuestionPlan,
    ) -> list[GeneratedQuestion]:
        questions: list[GeneratedQuestion] = []

        for item in plan.items:
            prompt = self._build_prompt(request, item.concept, item.difficulty, item.question_type)
            generated_text = self.llm_adapter.generate(prompt, request.model_to_use)

            options = self._build_options(item.question_type, item.concept)
            answer = self._build_answer(item.question_type, item.concept)

            questions.append(
                GeneratedQuestion(
                    question_id=f"Q{item.question_number:03d}",
                    subject=request.subject,
                    chapter=request.chapter,
                    concept=item.concept,
                    difficulty=item.difficulty,
                    question_type=item.question_type,
                    question_text=generated_text,
                    options=options,
                    correct_answer=answer,
                    explanation=f"This answer is based on the concept '{item.concept}'.",
                    marks=self._marks_by_difficulty(item.difficulty),
                    diagram_required=item.diagram_required,
                    diagram_prompt="",
                )
            )
        return questions

    def _build_prompt(
        self,
        request: QuestionGenerationRequest,
        concept: str,
        difficulty: Difficulty,
        question_type: QuestionType,
    ) -> str:
        return (
            f"Create one CBSE-style {question_type.value} question for subject '{request.subject}' "
            f"on chapter '{request.chapter}' around concept '{concept}' with {difficulty.value} difficulty."
        )

    def _build_options(self, question_type: QuestionType, concept: str) -> list[str]:
        if question_type != QuestionType.MCQ:
            return []
        return [
            f"{concept} option A",
            f"{concept} option B",
            f"{concept} option C",
            f"{concept} option D",
        ]

    def _build_answer(self, question_type: QuestionType, concept: str) -> str:
        if question_type == QuestionType.MCQ:
            return "A"
        if question_type == QuestionType.NUMERIC:
            return "42"
        return f"Key idea of {concept}"

    def _marks_by_difficulty(self, difficulty: Difficulty) -> int:
        return {Difficulty.EASY: 1, Difficulty.MEDIUM: 3, Difficulty.HARD: 5}[difficulty]
