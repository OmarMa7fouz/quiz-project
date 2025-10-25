"""
Script to view database contents
Run with: python scripts/view_database.py
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_quiz_project.settings')
django.setup()

from apps.quiz_app.models import  Subject, Question #, Answer, QuizResult, Quiz, UserAnswer
from django.contrib.auth.models import User


def print_separator(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def view_subjects():
    print_separator("Subjects")
    subjects = Subject.objects.all()
    if not subjects.exists():
        print("No subjects found.")
        return

    for subject in subjects:
        print(f"ID: {subject.id} | Code: {subject.code} | Name: {subject.name}")
        print(f"   Description: {subject.description}")
        print(f"   Total Questions: {subject.questions.count()}")
        print()



def view_questions():
    print_separator("Questions")
    questions = Question.objects.all().order_by('id')
    if not questions.exists():
        print("No questions found.")
        return

    for q in questions:
        print(f"ID: {q.id} | Subject: {q.subject.code} | Level: {q.level}")
        print(f"   Question: {q.question_text[:80]}")
        print(f"   A: {q.option_a}")
        print(f"   B: {q.option_b}")
        print(f"   C: {q.option_c}")
        print(f"   D: {q.option_d}")
        print(f"   Correct: {q.correct_answer}")
        print()



def view_statistics():
    print_separator("Statistics")
    print(f"Total Subjects: {Subject.objects.count()}")
    print(f"Total Questions: {Question.objects.count()}")
    print(f"Total Users: {User.objects.count()}")        

def main():
    print("\n" + "=" * 80)
    print("DATABASE VIEWER")
    print("=" * 80)

    view_statistics()
    view_subjects()
    view_questions()
    

    print("\n" + "=" * 80)
    print("Database viewing completed!")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()

