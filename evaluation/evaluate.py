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

WEAK_THRESHOLD = 0.5  # below 50% of a question's points = weak area


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


def evaluate_session(session_records, questions):
    """
    Evaluate every answer in a session.

    Args:
        session_records (list[dict]): Records with 'id', 'question', 'answer'.
        questions (list[dict]): The questions used (needed for keywords).

    Returns:
        dict: {'results': [...], 'total_score', 'max_total', 'weak_questions'}
    """
    keywords_by_id = {q["id"]: q["keywords"] for q in questions}

    results = []
    for record in session_records:
        evaluation = evaluate_answer(record["answer"], keywords_by_id[record["id"]])
        evaluation["id"] = record["id"]
        evaluation["question"] = record["question"]
        results.append(evaluation)

    total_score = sum(r["score"] for r in results)
    max_total = sum(r["max_score"] for r in results)
    weak_questions = [
        r["question"] for r in results
        if r["score"] / r["max_score"] < WEAK_THRESHOLD
    ]

    return {
        "results": results,
        "total_score": total_score,
        "max_total": max_total,
        "weak_questions": weak_questions,
    }
