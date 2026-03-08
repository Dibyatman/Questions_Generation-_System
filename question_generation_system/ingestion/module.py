from __future__ import annotations

import re
from typing import Protocol

from question_generation_system.models import ContentType, IngestionInput, StructuredContent


class OCRAdapter(Protocol):
    def extract_text(self, image_or_pdf_path: str) -> str:
        ...


class SimpleOCRAdapter:
    """Placeholder OCR adapter for local development."""

    def extract_text(self, image_or_pdf_path: str) -> str:
        return f"[OCR extracted content from {image_or_pdf_path}]"


class ContentIngestionModule:
    def __init__(self, ocr_adapter: OCRAdapter | None = None) -> None:
        self.ocr_adapter = ocr_adapter or SimpleOCRAdapter()

    def ingest(self, data: IngestionInput) -> StructuredContent:
        raw = data.raw_text or ""
        if not raw and data.image_path:
            raw = self.ocr_adapter.extract_text(data.image_path)
        elif not raw and data.pdf_path:
            raw = self.ocr_adapter.extract_text(data.pdf_path)

        content_type = self._detect_content_type(raw)
        formulas = self._extract_formulas(raw)
        diagrams = self._extract_diagram_hints(raw)

        return StructuredContent(
            content_type=content_type,
            normalized_text=raw.strip(),
            formulas=formulas,
            diagram_descriptions=diagrams,
            metadata={"source": "raw_text" if data.raw_text else "ocr"},
        )

    def _detect_content_type(self, text: str) -> ContentType:
        equation_pattern = r"(=|\b(sin|cos|tan|log|sqrt|integral|\^|\d+/\d+)\b)"
        diagram_pattern = r"\b(diagram|figure|label|draw|circuit|graph|map)\b"

        has_equation = re.search(equation_pattern, text, flags=re.IGNORECASE)
        has_diagram = re.search(diagram_pattern, text, flags=re.IGNORECASE)

        if has_diagram:
            return ContentType.DIAGRAM
        if has_equation:
            return ContentType.EQUATION
        return ContentType.TEXT

    def _extract_formulas(self, text: str) -> list[str]:
        return [line.strip() for line in text.splitlines() if "=" in line]

    def _extract_diagram_hints(self, text: str) -> list[str]:
        hints = []
        for line in text.splitlines():
            if re.search(r"\b(diagram|figure|graph|map|circuit)\b", line, flags=re.IGNORECASE):
                hints.append(line.strip())
        return hints
