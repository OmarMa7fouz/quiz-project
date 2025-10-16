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

from apps.quiz_app.models import Category, Quiz, Question, Answer, QuizResult, UserAnswer
from django.contrib.auth.models import User


def print_separator(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def view_categories():
    print_separator("الفئات | Categories")
    categories = Category.objects.all()
    for cat in categories:
        print(f"ID: {cat.id} | Name: {cat.name} | Slug: {cat.slug}")
        print(f"   Description: {cat.description}")
        print(f"   Icon: {cat.icon}")
        print()


def view_quizzes():
    print_separator("الاختبارات | Quizzes")
    quizzes = Quiz.objects.all()
    for quiz in quizzes:
        print(f"ID: {quiz.id} | Title: {quiz.title}")
        print(f"   Category: {quiz.category.name}")
        print(f"   Difficulty: {quiz.difficulty} | Duration: {quiz.duration} min")
        print(f"   Questions: {quiz.questions_count} | Pass %: {quiz.pass_percentage}%")
        print(f"   Active: {quiz.is_active} | Created: {quiz.created_at.strftime('%Y-%m-%d')}")
        print()


def view_questions():
    print_separator("الأسئلة | Questions")
    questions = Question.objects.all()
    for q in questions:
        print(f"ID: {q.id} | Quiz: {q.quiz.title}")
        print(f"   Question: {q.question_text[:80]}...")
        print(f"   Type: {q.question_type} | Points: {q.points}")
        if q.code_snippet:
            print(f"   Has Code: Yes")
        
        # Show answers
        answers = q.answers.all()
        print(f"   Answers ({answers.count()}):")
        for ans in answers:
            correct = "✓" if ans.is_correct else "✗"
            print(f"      {correct} {ans.answer_text}")
        print()


def view_users():
    print_separator("المستخدمين | Users")
    users = User.objects.all()
    for user in users:
        print(f"ID: {user.id} | Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Is Staff: {user.is_staff} | Is Superuser: {user.is_superuser}")
        print(f"   Date Joined: {user.date_joined.strftime('%Y-%m-%d %H:%M')}")
        
        # Show quiz results
        results = QuizResult.objects.filter(user=user)
        if results.exists():
            print(f"   Quiz Results ({results.count()}):")
            for result in results:
                print(f"      {result.quiz.title}: {result.percentage}% - {'Passed' if result.passed else 'Failed'}")
        print()


def view_quiz_results():
    print_separator("نتائج الاختبارات | Quiz Results")
    results = QuizResult.objects.all()
    
    if not results.exists():
        print("   No quiz results yet. Take a quiz to see results here!")
        return
    
    for result in results:
        print(f"ID: {result.id} | User: {result.user.username} | Quiz: {result.quiz.title}")
        print(f"   Score: {result.score}/{result.total_points} ({result.percentage}%)")
        print(f"   Passed: {'Yes ✓' if result.passed else 'No ✗'}")
        print(f"   Time Taken: {result.time_taken} seconds")
        print(f"   Completed: {result.completed} | Started: {result.started_at.strftime('%Y-%m-%d %H:%M')}")
        print()


def view_statistics():
    print_separator("إحصائيات | Statistics")
    
    print(f"📊 Total Categories: {Category.objects.count()}")
    print(f"📝 Total Quizzes: {Quiz.objects.count()}")
    print(f"❓ Total Questions: {Question.objects.count()}")
    print(f"✅ Total Answers: {Answer.objects.count()}")
    print(f"👥 Total Users: {User.objects.count()}")
    print(f"📈 Total Quiz Results: {QuizResult.objects.count()}")
    print(f"💬 Total User Answers: {UserAnswer.objects.count()}")
    
    # Active quizzes
    active_quizzes = Quiz.objects.filter(is_active=True).count()
    print(f"🟢 Active Quizzes: {active_quizzes}")
    
    # Completed results
    completed = QuizResult.objects.filter(completed=True).count()
    print(f"✓ Completed Quiz Attempts: {completed}")
    
    # Passed results
    passed = QuizResult.objects.filter(passed=True).count()
    print(f"🎉 Passed Attempts: {passed}")


def main():
    print("\n" + "🗄️ " * 20)
    print("DATABASE VIEWER - عارض قاعدة البيانات")
    print("🗄️ " * 20)
    
    # Show all data
    view_statistics()
    view_categories()
    view_quizzes()
    view_questions()
    view_users()
    view_quiz_results()
    
    print("\n" + "=" * 80)
    print("✅ Database viewing completed!")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()

