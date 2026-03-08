from __future__ import annotations

import re
from collections import Counter

from question_generation_system.models import ConceptExtractionOutput, ConceptTag, StructuredContent


class ConceptExtractionModule:
    """Extract topics/formulas/concepts from structured chapter content."""

    STOP_WORDS = {
        "the", "is", "a", "an", "and", "of", "to", "in", "on", "for", "with",
        "as", "by", "that", "this", "be", "are", "from", "or", "at", "it", "we",
    }

    def extract(self, content: StructuredContent, max_topics: int = 8) -> ConceptExtractionOutput:
        tokens = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", content.normalized_text.lower())
        filtered = [t for t in tokens if t not in self.STOP_WORDS]
        counter = Counter(filtered)

        key_topics = [token for token, _ in counter.most_common(max_topics)]
        concepts = [
            ConceptTag(concept=topic.title(), concept_type="topic", weight=float(weight))
            for topic, weight in counter.most_common(max_topics)
        ]

        for formula in content.formulas:
            concepts.append(ConceptTag(concept=formula, concept_type="formula", weight=1.5))

        return ConceptExtractionOutput(
            key_topics=[t.title() for t in key_topics],
            formulas=content.formulas,
            concepts=concepts,
        )
