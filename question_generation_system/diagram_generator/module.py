from __future__ import annotations

from question_generation_system.models import GeneratedQuestion


class DiagramPromptGenerator:
    def attach_diagram_prompts(self, questions: list[GeneratedQuestion]) -> list[GeneratedQuestion]:
        for question in questions:
            if question.diagram_required:
                question.diagram_prompt = (
                    f"Educational line diagram for concept '{question.concept}' in {question.subject}, "
                    f"suitable for CBSE {question.difficulty.value} level question."
                )
        return questions
