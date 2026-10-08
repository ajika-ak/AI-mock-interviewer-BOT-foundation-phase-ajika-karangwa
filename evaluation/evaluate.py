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


def evaluate_answer(answer, keywords):
    """
    Score a single answer against a question's keywords.

    Args:
        answer (str): The candidate's answer text.
        keywords (list[str]): Expected keywords for the question.

    Returns:
        dict: {'score', 'max_score', 'matched', 'missed', 'feedback'}
    """
    matched = [kw for kw in keywords if keyword_found(kw, answer)]
    missed = [kw for kw in keywords if kw not in matched]

    if not answer.strip():
        feedback = "No answer given."
    elif not missed:
        feedback = "Great answer - all key concepts covered."
    elif not matched:
        feedback = f"Key concepts missing. Revise: {', '.join(missed)}."
    else:
        feedback = f"Good start. Also mention: {', '.join(missed)}."

    return {
        "score": len(matched),
        "max_score": len(keywords),
        "matched": matched,
        "missed": missed,
        "feedback": feedback,
    }
