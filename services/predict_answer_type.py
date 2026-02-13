"""
Predicts a suitable question/answer type from the question text (Answer genius).
Uses keyword and phrase matching; only suggests types that can be auto-applied.
"""
import re
from typing import Literal

PredictableType = Literal["Single text box", "Multiple choice", "Checkboxes"]

RULES: list[tuple[PredictableType, list[str]]] = [
    (
        "Single text box",
        [
            r"enter\s+your\s+name",
            r"what\s+is\s+your\s+name",
            r"your\s+name",
            r"enter\s+name",
            r"name\s*$",
            r"email\s*(address)?",
            r"enter\s+your\s+email",
            r"what\s+is\s+your\s+email",
            r"phone\s*(number)?",
            r"enter\s+your\s+phone",
            r"address",
            r"enter\s+your\s+address",
            r"company\s+name",
            r"job\s+title",
            r"how\s+old\s+are\s+you",
            r"age\s*$",
            r"enter\s+your",
            r"please\s+provide\s+your",
            r"type\s+your",
            r"write\s+your",
        ],
    ),
    (
        "Multiple choice",
        [
            r"select\s+your\s+preference",
            r"select\s+(one|a)\s+option",
            r"choose\s+(one|your)",
            r"which\s+one\s+(do\s+you|would\s+you)",
            r"pick\s+(one|your)",
            r"what\s+is\s+your\s+preference",
            r"prefer",
            r"select\s+from\s+the",
            r"choose\s+from",
            r"which\s+(option|choice)",
            r"how\s+would\s+you\s+rate",
            r"rate\s+your\s+experience",
            r"select\s+the\s+(best|option)",
            r"choose\s+the\s+(best|option)",
            r"one\s+of\s+the\s+following",
            r"select\s+one",
            r"choose\s+one",
            r"pick\s+one",
            r"which\s+of\s+these",
            r"select\s+your",
            r"choose\s+your",
        ],
    ),
    (
        "Checkboxes",
        [
            r"select\s+all\s+that\s+apply",
            r"check\s+all\s+that\s+apply",
            r"which\s+of\s+the\s+following",
            r"select\s+all",
            r"check\s+all",
            r"select\s+any",
            r"choose\s+all",
            r"which\s+apply",
            r"tick\s+all",
            r"mark\s+all",
        ],
    ),
]

# Precompile regexes
COMPILED_RULES: list[tuple[PredictableType, list[re.Pattern]]] = [
    (answer_type, [re.compile(p, re.IGNORECASE) for p in patterns])
    for answer_type, patterns in RULES
]


def predict_answer_type(question_text: str) -> PredictableType | None:
    """Returns the best matching answer type for the question text, or None if no match."""
    trimmed = question_text.strip()
    if not trimmed:
        return None

    for answer_type, patterns in COMPILED_RULES:
        for pattern in patterns:
            if pattern.search(trimmed):
                return answer_type
    return None
