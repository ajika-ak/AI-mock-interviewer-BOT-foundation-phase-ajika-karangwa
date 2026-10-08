"""
Evaluation Engine (Basic Scoring)
------------------------------------------
Scores each answer by keyword matching against the question's
'keywords' list from questions.json:

    - Each keyword found in the answer = 1 point
    - Max score for a question = number of keywords it has
    - Missed keywords become feedback ("revise: ...")

Matching rules:
    - Case-insensitive ("For" matches "for")
    - Whole-word only, so keyword "list" does NOT match "listen"
    - Simple plurals are accepted ("lists" matches "list")
"""

import re


def keyword_found(keyword, answer):
    """Return True if the keyword appears in the answer as a whole word."""
    pattern = r"\b" + re.escape(keyword.lower()) + r"(?:s|es)?\b"
    return re.search(pattern, answer.lower()) is not None
