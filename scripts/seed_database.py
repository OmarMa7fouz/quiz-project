"""
Seed script to populate the database with sample data
Run this script with:
python scripts/seed_database.py
"""
import os  # used to build paths and interact with the OS
import sys  # used to modify sys.path so Django settings can be discovered
import django  # Django framework import to initialize project environment

# Setup Django environment so this standalone script can use ORM models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # add project root to PYTHONPATH
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_quiz_project.settings')  # set Django settings module
django.setup()  # initialize Django

from apps.quiz_app.models import Subject, Question  # import Subject and Question models from app


def create_subjects():  # function to create the four main subjects
    """Create the 4 main subjects"""  # docstring describing purpose
    subjects_data = [  # list of subject dictionaries to create
        {
            'code': 'CSW351-AI',  # subject code
            'name': 'Artificial Intelligence',  # human readable name
            'description': 'AI concepts, machine learning, neural networks, and intelligent systems'  # description
        },
        {
            'code': 'INT353-MULTIMEDIA',  # subject code
            'name': 'Multimedia',  # name
            'description': 'Multimedia systems, graphics, audio, video processing, and compression'  # description
        },
        {
            'code': 'INT341-WEB-TECHNOLOGY',  # subject code
            'name': 'Web Technology',  # name
            'description': 'Web development, HTML, CSS, JavaScript, and modern web frameworks'  # description
        },
        {
            'code': 'CSW325-PARALLEL-PROCESSING',  # subject code
            'name': 'Parallel Processing',  # name
            'description': 'Parallel computing, multi-threading, distributed systems, and concurrent programming'  # description
        },
    ]

    print("=" * 80)  # visual separator
    print("CREATING SUBJECTS")  # header
    print("=" * 80)  # visual separator
    
    for data in subjects_data:  # iterate over each subject definition
        subject, created = Subject.objects.get_or_create(  # get or create Subject row
            code=data['code'],  # lookup by code
            defaults=data  # defaults to set if created
        )
        if created:  # if newly created
            print(f"[+] Created: {subject.code} - {subject.name}")  # show created message
        else:  # if already existed
            print(f"[=] Exists: {subject.code} - {subject.name}")  # show exists message
    
    print()  # blank line for readability
    return Subject.objects.all()  # return queryset of all subjects


def create_placeholder_questions(subject, level, count=30):
    """Create placeholder questions for a subject and level (safe from duplicates)"""
    questions_created = 0
    existing_questions = Question.objects.filter(subject=subject, level=level)
    existing_count = existing_questions.count()

    # skip creation if already have 30
    if existing_count >= count:
        print(f"  [=] {level.upper():10} - Already has {existing_count} questions, skipping")
        return 0

    start_index = existing_count + 1
    for i in range(start_index, count + 1):
        question_text = f"[{subject.code}] [{level.upper()}] Question {i}: Replace this with your actual question"
        Question.objects.create(
            subject=subject,
            question_text=question_text,
            level=level,
            option_a='Option A - Replace with actual answer',
            option_b='Option B - Replace with actual answer',
            option_c='Option C - Replace with actual answer',
            option_d='Option D - Replace with actual answer',
            correct_answer='A',
            explanation=f'Add explanation for question {i} here'
        )
        questions_created += 1

    return questions_created


def create_all_questions(subjects):
    """Create 30 placeholder questions for each level per subject"""
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
            print(f"  [+] {level.upper():10} - Added {count} new questions")
        total_questions += subject_total
        print(f"  Total for {subject.code}: {subject_total} questions")

    return total_questions


def main():  # main entry point for the seeding script
    """Main seeding function"""  # docstring
    print("\n" + "=" * 80)  # header separator
    print("DATABASE SEEDING STARTED")  # title
    print("=" * 80 + "\n")  # separator and newline
    
    # Clear existing data  # prompt user whether to wipe existing subjects/questions
    confirm = input("Clear existing data? (yes/no): ").strip().lower()  # read user confirmation
    if confirm == 'yes':  # if user confirms
        deleted_questions = Question.objects.all().count()  # count questions
        deleted_subjects = Subject.objects.all().count()  # count subjects
        Question.objects.all().delete()  # delete all questions
        Subject.objects.all().delete()  # delete all subjects
        print(f"[+] Cleared {deleted_questions} questions and {deleted_subjects} subjects\n")  # report
    
    # Create subjects  # invoke subject creation
    subjects = create_subjects()  # create or fetch subjects
    
    # Create placeholder questions (360 total)  # create placeholders for each subject/level
    total_questions = create_all_questions(subjects)  # create and collect total
    
    # Summary  # print final summary
    print("=" * 80)  # separator
    print("DATABASE SEEDING COMPLETED")  # completion heading
    print("=" * 80)  # separator
    print(f"Total Subjects: {subjects.count()}")  # print number of subjects
    print(f"Total Questions: {total_questions}")  # print total created
    print(f"\nStructure:")  # structure heading
    print(f"  - 4 Subjects")  # note subjects count
    print(f"  - 3 Levels per subject (easy, medium, hard)")  # levels info
    print(f"  - 30 Questions per level")  # per-level count
    print(f"  - Total: {subjects.count()} × 3 × 30 = {total_questions} questions")  # total math
    print(f"\nNext Steps:")  # next steps heading
    print(f"1. Edit questions in database directly using SQL or Python script")  # instruction 1
    print(f"2. Or replace placeholder text with actual questions")  # instruction 2
    print(f"3. Run server: python manage.py runserver")  # instruction 3
    print(f"4. Visit: http://127.0.0.1:8000/")  # instruction 4
    print("=" * 80 + "\n")  # closing separator


if __name__ == '__main__':  # run main when script executed directly
    main()  # call main()
