from __future__ import annotations

from itertools import cycle

from question_generation_system.models import (
    ConceptExtractionOutput,
    Difficulty,
    QuestionGenerationRequest,
    QuestionPlan,
    QuestionPlanItem,
    QuestionType,
)


class QuestionPlanningEngine:
    """Creates a generation plan based on distribution and constraints."""

    def create_plan(
        self,
        request: QuestionGenerationRequest,
        extracted_concepts: ConceptExtractionOutput,
    ) -> QuestionPlan:
        difficulties = (
            [Difficulty.EASY] * request.difficulty_distribution.easy
            + [Difficulty.MEDIUM] * request.difficulty_distribution.medium
            + [Difficulty.HARD] * request.difficulty_distribution.hard
        )

        q_types = self._build_question_type_sequence(request)
        concept_cycle = cycle(self._concept_list(extracted_concepts))

        items: list[QuestionPlanItem] = []
        for idx in range(request.total_questions):
            items.append(
                QuestionPlanItem(
                    question_number=idx + 1,
                    difficulty=difficulties[idx],
                    question_type=q_types[idx],
                    concept=next(concept_cycle),
                    diagram_required=request.diagram_required and idx % 3 == 0,
                )
            )
        return QuestionPlan(items=items)

    def _build_question_type_sequence(self, request: QuestionGenerationRequest) -> list[QuestionType]:
        sequence: list[QuestionType] = []
        numeric_assigned = 0

        for _ in range(request.total_questions):
            if numeric_assigned < request.numeric_questions:
                sequence.append(QuestionType.NUMERIC)
                numeric_assigned += 1
            else:
                valid_non_numeric = [q for q in request.question_types if q != QuestionType.NUMERIC]
                sequence.append(valid_non_numeric[len(sequence) % max(1, len(valid_non_numeric))])
        return sequence

    def _concept_list(self, extracted_concepts: ConceptExtractionOutput) -> list[str]:
        concepts = [c.concept for c in extracted_concepts.concepts if c.concept_type == "topic"]
        return concepts or ["General Understanding"]
