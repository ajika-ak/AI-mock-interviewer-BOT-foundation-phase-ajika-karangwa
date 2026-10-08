from .question_bank import ask_question

def run_interview(questions):
    """
    Run a full interview session: ask each selected question and
    collect the candidate's answers.
    """
    session_records = []

    for i, question in enumerate(questions, start=1):
        print(f"\n--- Question {i} of {len(questions)} ---")
        answer = ask_question(question)

        session_records.append({
            "id": question["id"],
            "question": question["question"],
            "answer": answer
        })

    return session_records