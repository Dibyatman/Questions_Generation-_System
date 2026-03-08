# Question Generation System (QGS)

A modular Python system for generating CBSE-style exam questions from chapter content containing:
- text-only content,
- text with equations,
- text with diagrams.

## Project Structure

```text
question_generation_system/
  ingestion/
  concept_extraction/
  planning_engine/
  question_generator/
  diagram_generator/
  validator/
  api/
  models.py
  pipeline.py
main.py
```

## Modules

1. **Content Ingestion Module**
   - Input: raw text / image / PDF path
   - Detects text/equation/diagram style content
   - Uses OCR adapter abstraction for image/PDF extraction

2. **Concept Extraction Module**
   - Extracts topics and formulas
   - Produces concept tags for downstream planning

3. **Question Planning Engine**
   - Consumes request constraints and concepts
   - Produces a question-by-question plan for difficulty/type/concept

4. **Question Generation Module**
   - LLM adapter interface for pluggable model providers
   - Generates question text, options, answers, explanations, and marks

5. **Diagram Prompt Generator**
   - Adds diagram prompts for diagram-required questions

6. **Question Validation Module**
   - Duplicate detection
   - Numeric answer validation
   - Clarity and difficulty consistency checks

7. **Output Formatter**
   - Unified JSON response through Pydantic response model

## API

### Endpoint
`POST /generate_questions`

### Example request

```json
{
  "subject": "Physics",
  "chapter": "Laws of Motion",
  "chapter_content": "Newton's second law is F = ma. Draw a free body diagram.",
  "total_questions": 10,
  "difficulty_distribution": {
    "easy": 3,
    "medium": 4,
    "hard": 3
  },
  "numeric_questions": 2,
  "diagram_required": true,
  "question_types": ["MCQ", "numeric"],
  "model_to_use": "mock-llm"
}
```

## Run

```bash
pip install fastapi uvicorn pydantic
uvicorn main:app --reload
```

## Example usage (standalone pipeline)

```bash
python -m question_generation_system.example_usage
```

## Extending to real LLM/VLM models

- Replace `MockLLMAdapter` with adapters for Claude/GPT/Gemini/open-source models.
- Replace `SimpleOCRAdapter` with OCR/VLM integrations.
- Keep interface contracts intact to preserve module-level independence.
