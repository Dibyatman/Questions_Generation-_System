from __future__ import annotations

from question_generation_system.concept_extraction import ConceptExtractionModule
from question_generation_system.diagram_generator import DiagramPromptGenerator
from question_generation_system.ingestion import ContentIngestionModule
from question_generation_system.models import IngestionInput, QuestionGenerationRequest, QuestionGenerationResponse
from question_generation_system.planning_engine import QuestionPlanningEngine
from question_generation_system.question_generator import QuestionGenerationModule
from question_generation_system.validator import QuestionValidationModule


class QuestionGenerationPipeline:
    def __init__(self) -> None:
        self.ingestion = ContentIngestionModule()
        self.concept_extractor = ConceptExtractionModule()
        self.planner = QuestionPlanningEngine()
        self.generator = QuestionGenerationModule()
        self.diagram_generator = DiagramPromptGenerator()
        self.validator = QuestionValidationModule()

    def run(self, request: QuestionGenerationRequest) -> QuestionGenerationResponse:
        structured = self.ingestion.ingest(IngestionInput(raw_text=request.chapter_content))
        concepts = self.concept_extractor.extract(structured)
        plan = self.planner.create_plan(request, concepts)
        questions = self.generator.generate(request, plan)
        questions = self.diagram_generator.attach_diagram_prompts(questions)
        validated_questions, warnings = self.validator.validate(questions)

        return QuestionGenerationResponse(
            questions=validated_questions,
            metadata={
                "content_type": structured.content_type.value,
                "formula_count": len(structured.formulas),
                "concept_count": len(concepts.concepts),
                "warnings": warnings,
            },
        )
