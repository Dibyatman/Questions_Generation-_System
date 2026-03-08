from __future__ import annotations

from collections import Counter

from question_generation_system.models import GeneratedQuestion, QuestionType


class QuestionValidationModule:
    def validate(self, questions: list[GeneratedQuestion]) -> tuple[list[GeneratedQuestion], list[str]]:
        warnings: list[str] = []

        warnings.extend(self._check_duplicates(questions))
        warnings.extend(self._check_numeric_answers(questions))
        warnings.extend(self._check_clarity(questions))
        warnings.extend(self._check_difficulty_consistency(questions))

        return questions, warnings

    def _check_duplicates(self, questions: list[GeneratedQuestion]) -> list[str]:
        texts = [q.question_text for q in questions]
        duplicates = [text for text, count in Counter(texts).items() if count > 1]
        return [f"Duplicate question detected: {dup[:80]}" for dup in duplicates]

    def _check_numeric_answers(self, questions: list[GeneratedQuestion]) -> list[str]:
        warnings = []
        for q in questions:
            if q.question_type == QuestionType.NUMERIC:
                try:
                    float(q.correct_answer)
                except ValueError:
                    warnings.append(f"Numeric question {q.question_id} has non-numeric answer.")
        return warnings

    def _check_clarity(self, questions: list[GeneratedQuestion]) -> list[str]:
        warnings = []
        for q in questions:
            if len(q.question_text.split()) < 6:
                warnings.append(f"Question {q.question_id} may be unclear (too short).")
        return warnings

    def _check_difficulty_consistency(self, questions: list[GeneratedQuestion]) -> list[str]:
        warnings = []
        for q in questions:
            if q.difficulty.value == "hard" and q.marks < 5:
                warnings.append(f"Question {q.question_id} marked hard but low marks assigned.")
        return warnings
