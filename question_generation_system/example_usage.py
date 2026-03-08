from question_generation_system.models import DifficultyDistribution, QuestionGenerationRequest, QuestionType
from question_generation_system.pipeline import QuestionGenerationPipeline


if __name__ == "__main__":
    pipeline = QuestionGenerationPipeline()

    request = QuestionGenerationRequest(
        subject="Physics",
        chapter="Laws of Motion",
        chapter_content="Newton's second law is F = ma. Draw a free body diagram for a block on incline.",
        total_questions=4,
        difficulty_distribution=DifficultyDistribution(easy=1, medium=2, hard=1),
        numeric_questions=1,
        diagram_required=True,
        question_types=[QuestionType.MCQ, QuestionType.NUMERIC, QuestionType.SHORT_ANSWER],
        model_to_use="mock-llm",
    )

    response = pipeline.run(request)
    print(response.model_dump_json(indent=2))
