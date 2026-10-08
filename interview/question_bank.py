"""
Question Bank & CLI Flow
------------------------------------------
Loads a Python question bank from questions.json, randomly selects a
set of questions, and runs a simple terminal-based Q&A session that
collects the candidate's text answers.
"""

import json
import random


NUM_QUESTIONS_PER_SESSION = 5

def load_questions(file_path):
    with open(file_path, "r") as file:
        questions = json.load(file)
    return questions


def select_random_questions(questions, count=NUM_QUESTIONS_PER_SESSION):
    # random.sample picks unique items -- no question repeats in one session
    count = min(count, len(questions))
    return random.sample(questions, count)


def ask_question(question):
    print(f"\nQuestion: {question['question']}")
    answer = input("Your answer: ").strip()
    return answer