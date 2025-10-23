"""
Seed script to populate the database with sample data
Run this script with:
python scripts/seed_database.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_quiz_project.settings')
django.setup()

from apps.quiz_app.models import Subject, Question


def create_subjects():
    """Create the 4 main subjects"""
    subjects_data = [
        {
            'code': 'CSW351-AI',
            'name': 'Artificial Intelligence',
            'description': 'AI concepts, machine learning, neural networks, and intelligent systems'
        },
        {
            'code': 'INT353-MULTIMEDIA',
            'name': 'Multimedia',
            'description': 'Multimedia systems, graphics, audio, video processing, and compression'
        },
        {
            'code': 'INT341-WEB-TECHNOLOGY',
            'name': 'Web Technology',
            'description': 'Web development, HTML, CSS, JavaScript, and modern web frameworks'
        },
        {
            'code': 'CSW325-PARALLEL-PROCESSING',
            'name': 'Parallel Processing',
            'description': 'Parallel computing, multi-threading, distributed systems, and concurrent programming'
        },
    ]

    print("=" * 80)
    print("CREATING SUBJECTS")
    print("=" * 80)
    
    for data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        if created:
            print(f"[+] Created: {subject.code} - {subject.name}")
        else:
            print(f"[=] Exists: {subject.code} - {subject.name}")
    
    print()
    return Subject.objects.all()


def create_placeholder_questions(subject, level, count=30):
    """
    Create placeholder questions for a subject and level
    
    Args:
        subject: Subject object
        level: Difficulty level (easy, medium, hard)
        count: Number of questions to create (default: 30)
    """
    questions_created = 0
    
    for i in range(1, count + 1):
        question_text = f"[{subject.code}] [{level.upper()}] Question {i}: Replace this with your actual question"
        
        question, created = Question.objects.get_or_create(
            subject=subject,
            question_text=question_text,
            level=level,
            defaults={
                'option_a': f'Option A - Replace with actual answer',
                'option_b': f'Option B - Replace with actual answer',
                'option_c': f'Option C - Replace with actual answer',
                'option_d': f'Option D - Replace with actual answer',
                'correct_answer': 'A',
                'explanation': f'Add explanation for question {i} here'
            }
        )
        
        if created:
            questions_created += 1
    
    return questions_created


def create_all_questions(subjects):
    """Create 30 placeholder questions for each level for each subject"""
    print("=" * 80)
    print("CREATING QUESTIONS (30 per level per subject)")
    print("=" * 80)
    
    levels = ['easy', 'medium', 'hard']
    total_questions = 0
    
    for subject in subjects:
        print(f"\n{subject.code}:")
        subject_total = 0
        
        for level in levels:
            count = create_placeholder_questions(subject, level, count=30)
            subject_total += count
            print(f"  [+] {level.upper():10} - Created {count} placeholder questions")
        
        total_questions += subject_total
        print(f"  Total for {subject.code}: {subject_total} questions")
    
    print()
    return total_questions


def main():
    """Main seeding function"""
    print("\n" + "=" * 80)
    print("DATABASE SEEDING STARTED")
    print("=" * 80 + "\n")
    
    # Clear existing data
    confirm = input("Clear existing data? (yes/no): ").strip().lower()
    if confirm == 'yes':
        deleted_questions = Question.objects.all().count()
        deleted_subjects = Subject.objects.all().count()
        Question.objects.all().delete()
        Subject.objects.all().delete()
        print(f"[+] Cleared {deleted_questions} questions and {deleted_subjects} subjects\n")
    
    # Create subjects
    subjects = create_subjects()
    
    # Create placeholder questions (360 total)
    total_questions = create_all_questions(subjects)
    
    # Summary
    print("=" * 80)
    print("DATABASE SEEDING COMPLETED")
    print("=" * 80)
    print(f"Total Subjects: {subjects.count()}")
    print(f"Total Questions: {total_questions}")
    print(f"\nStructure:")
    print(f"  - 4 Subjects")
    print(f"  - 3 Levels per subject (easy, medium, hard)")
    print(f"  - 30 Questions per level")
    print(f"  - Total: {subjects.count()} × 3 × 30 = {total_questions} questions")
    print(f"\nNext Steps:")
    print(f"1. Edit questions in database directly using SQL or Python script")
    print(f"2. Or replace placeholder text with actual questions")
    print(f"3. Run server: python manage.py runserver")
    print(f"4. Visit: http://127.0.0.1:8000/")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()
