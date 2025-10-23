"""
Script to manage questions directly in database
No admin panel needed!

Usage:
    python scripts/manage_questions.py
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_quiz_project.settings')
django.setup()

from apps.quiz_app.models import Subject, Question


def list_subjects():
    """List all subjects"""
    print("\n" + "=" * 80)
    print("AVAILABLE SUBJECTS")
    print("=" * 80)
    subjects = Subject.objects.all()
    for i, subject in enumerate(subjects, 1):
        total = subject.questions.count()
        easy = subject.questions.filter(level='easy').count()
        medium = subject.questions.filter(level='medium').count()
        hard = subject.questions.filter(level='hard').count()
        print(f"{i}. {subject.code}")
        print(f"   Name: {subject.name}")
        print(f"   Questions: {total} total (Easy: {easy}, Medium: {medium}, Hard: {hard})")
    print("=" * 80)


def list_questions(subject_code, level):
    """List questions for a subject and level"""
    try:
        subject = Subject.objects.get(code=subject_code)
        questions = Question.objects.filter(subject=subject, level=level).order_by('id')
        
        print("\n" + "=" * 80)
        print(f"QUESTIONS: {subject.code} - {level.upper()}")
        print("=" * 80)
        
        for i, q in enumerate(questions, 1):
            print(f"\n{i}. ID: {q.id}")
            print(f"   Question: {q.question_text[:80]}...")
            print(f"   A) {q.option_a[:50]}...")
            print(f"   B) {q.option_b[:50]}...")
            print(f"   C) {q.option_c[:50]}...")
            print(f"   D) {q.option_d[:50]}...")
            print(f"   Correct: {q.correct_answer}")
        
        print("\n" + "=" * 80)
        print(f"Total: {questions.count()} questions")
        print("=" * 80)
        
    except Subject.DoesNotExist:
        print(f"\n❌ Subject '{subject_code}' not found!")


def add_question():
    """Add a new question interactively"""
    print("\n" + "=" * 80)
    print("ADD NEW QUESTION")
    print("=" * 80)
    
    # Select subject
    subjects = Subject.objects.all()
    print("\nAvailable subjects:")
    for i, subject in enumerate(subjects, 1):
        print(f"{i}. {subject.code}")
    
    choice = input("\nSelect subject number: ").strip()
    try:
        subject = list(subjects)[int(choice) - 1]
    except:
        print("❌ Invalid choice!")
        return
    
    # Select level
    print("\nLevels: 1) easy  2) medium  3) hard")
    level_choice = input("Select level: ").strip()
    levels = {'1': 'easy', '2': 'medium', '3': 'hard'}
    level = levels.get(level_choice, 'easy')
    
    # Get question data
    print("\nEnter question details:")
    question_text = input("Question: ")
    option_a = input("Option A: ")
    option_b = input("Option B: ")
    option_c = input("Option C: ")
    option_d = input("Option D: ")
    correct = input("Correct answer (A/B/C/D): ").upper()
    explanation = input("Explanation (optional): ")
    
    # Create question
    Question.objects.create(
        subject=subject,
        question_text=question_text,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_answer=correct,
        level=level,
        explanation=explanation
    )
    
    print("\n✅ Question added successfully!")


def update_question():
    """Update an existing question"""
    print("\n" + "=" * 80)
    print("UPDATE QUESTION")
    print("=" * 80)
    
    question_id = input("\nEnter question ID: ").strip()
    
    try:
        question = Question.objects.get(id=question_id)
        
        print(f"\nCurrent question:")
        print(f"Question: {question.question_text}")
        print(f"A) {question.option_a}")
        print(f"B) {question.option_b}")
        print(f"C) {question.option_c}")
        print(f"D) {question.option_d}")
        print(f"Correct: {question.correct_answer}")
        
        print("\nEnter new values (press Enter to keep current):")
        
        new_text = input(f"Question [{question.question_text[:50]}...]: ")
        if new_text:
            question.question_text = new_text
        
        new_a = input(f"Option A [{question.option_a[:30]}...]: ")
        if new_a:
            question.option_a = new_a
        
        new_b = input(f"Option B [{question.option_b[:30]}...]: ")
        if new_b:
            question.option_b = new_b
        
        new_c = input(f"Option C [{question.option_c[:30]}...]: ")
        if new_c:
            question.option_c = new_c
        
        new_d = input(f"Option D [{question.option_d[:30]}...]: ")
        if new_d:
            question.option_d = new_d
        
        new_correct = input(f"Correct answer [{question.correct_answer}]: ").upper()
        if new_correct:
            question.correct_answer = new_correct
        
        new_explanation = input(f"Explanation: ")
        if new_explanation:
            question.explanation = new_explanation
        
        question.save()
        print("\n✅ Question updated successfully!")
        
    except Question.DoesNotExist:
        print(f"\n❌ Question ID {question_id} not found!")


def delete_question():
    """Delete a question"""
    print("\n" + "=" * 80)
    print("DELETE QUESTION")
    print("=" * 80)
    
    question_id = input("\nEnter question ID: ").strip()
    
    try:
        question = Question.objects.get(id=question_id)
        print(f"\nQuestion: {question.question_text[:80]}...")
        
        confirm = input("Are you sure you want to delete this? (yes/no): ").lower()
        if confirm == 'yes':
            question.delete()
            print("\n✅ Question deleted successfully!")
        else:
            print("\n❌ Deletion cancelled")
            
    except Question.DoesNotExist:
        print(f"\n❌ Question ID {question_id} not found!")


def show_menu():
    """Show main menu"""
    print("\n" + "=" * 80)
    print("📝 QUESTION MANAGER (No Admin Needed!)")
    print("=" * 80)
    print("\n1. List all subjects")
    print("2. List questions (by subject & level)")
    print("3. Add new question")
    print("4. Update question")
    print("5. Delete question")
    print("6. Exit")


def main():
    """Main function"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       📝 QUESTION MANAGER                                    ║
║                                                                              ║
║  Manage questions directly in database - No admin panel needed!             ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        show_menu()
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        
        if choice == '1':
            list_subjects()
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            subject_code = input("\nEnter subject code (e.g., CSW351-AI): ").strip().upper()
            level = input("Enter level (easy/medium/hard): ").strip().lower()
            list_questions(subject_code, level)
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            add_question()
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            update_question()
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            delete_question()
            input("\nPress Enter to continue...")
        
        elif choice == '6':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid choice!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

