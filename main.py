from pathlib import Path
from interview.question_bank import *
from interview.interview_process import *

project_root_path = Path(__file__).resolve().parent
QUESTIONS_FILE = project_root_path/ "data"/ "questions.json"


def main():
    print("=== Python Mock Interview ===")

    all_questions = load_questions(QUESTIONS_FILE)
    selected_questions = select_random_questions(all_questions)

    session_records = run_interview(selected_questions)

    print("\n=== Session Complete ===")
    print(f"You answered {len(session_records)} questions.\n")
    for record in session_records:
        print(f"Q{record['id']}: {record['question']}")
        print(f"A: {record['answer']}\n")


# Entry point
if __name__ == '__main__':
    main()

