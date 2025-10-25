"""  # top-level script docstring describing purpose and usage
Script to manage questions directly in database  # explains script function
No admin panel needed!  # short note

Usage:  # how to run the script
    python scripts/manage_questions.py  # example invocation
"""

import os  # import operating system helpers
import sys  # import system-specific params and functions
import django  # import Django to setup project environment

# Setup Django environment so models can be used standalone from scripts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # add project root to PYTHONPATH
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_quiz_project.settings')  # point to Django settings module
django.setup()  # initialize Django

from apps.quiz_app.models import Subject, Question  # import app models used by the script


def list_subjects():  # function to print a summary of available subjects
    """List all subjects"""  # docstring
    print("\n" + "=" * 80)  # visual separator
    print("AVAILABLE SUBJECTS")  # header text
    print("=" * 80)  # separator
    subjects = Subject.objects.all()  # queryset for all subjects
    for i, subject in enumerate(subjects, 1):  # enumerate subjects starting at 1
        total = subject.questions.count()  # total related questions (uses related_name 'questions')
        easy = subject.questions.filter(level='easy').count()  # count easy level
        medium = subject.questions.filter(level='medium').count()  # count medium level
        hard = subject.questions.filter(level='hard').count()  # count hard level
        print(f"{i}. {subject.code}")  # print subject index and code
        print(f"   Name: {subject.name}")  # print subject name
        print(f"   Questions: {total} total (Easy: {easy}, Medium: {medium}, Hard: {hard})")  # print counts
    print("=" * 80)  # closing separator


def list_questions(subject_code, level):  # function to list questions for a subject and difficulty level
    """List questions for a subject and level"""  # docstring
    try:
        subject = Subject.objects.get(code=subject_code)  # get subject by code (raises if missing)
        questions = Question.objects.filter(subject=subject, level=level).order_by('id')  # queryset filtered and ordered
        
        print("\n" + "=" * 80)  # header separator
        print(f"QUESTIONS: {subject.code} - {level.upper()}")  # header showing subject and level
        print("=" * 80)  # separator
        
        for i, q in enumerate(questions, 1):  # iterate and enumerate questions
            print(f"\n{i}. ID: {q.id}")  # print question index and DB id
            print(f"   Question: {q.question_text[:80]}...")  # show trimmed question text
            print(f"   A) {q.option_a[:50]}...")  # show trimmed option A
            print(f"   B) {q.option_b[:50]}...")  # show trimmed option B
            print(f"   C) {q.option_c[:50]}...")  # show trimmed option C
            print(f"   D) {q.option_d[:50]}...")  # show trimmed option D
            print(f"   Correct: {q.correct_answer}")  # show correct option letter
        
        print("\n" + "=" * 80)  # footer separator
        print(f"Total: {questions.count()} questions")  # print total count for this query
        print("=" * 80)  # closing separator
        
    except Subject.DoesNotExist:  # handle missing subject case
        print(f"\n❌ Subject '{subject_code}' not found!")  # user-friendly error


def add_question():  # interactive function to add a new question
    """Add a new question interactively"""  # docstring
    print("\n" + "=" * 80)  # header separator
    print("ADD NEW QUESTION")  # header text
    print("=" * 80)  # separator
    
    # Select subject  # prompt user to choose a subject
    subjects = Subject.objects.all()  # fetch all subjects
    print("\nAvailable subjects:")  # show available subjects
    for i, subject in enumerate(subjects, 1):  # list them with numbers
        print(f"{i}. {subject.code}")  # print code for selection
    
    choice = input("\nSelect subject number: ").strip()  # read user's choice and strip whitespace
    try:
        subject = list(subjects)[int(choice) - 1]  # convert to index and select subject
    except:  # catch any conversion/index errors
        print("❌ Invalid choice!")  # show error
        return  # abort function
    
    # Select level  # prompt for difficulty level
    print("\nLevels: 1) easy  2) medium  3) hard")  # show options
    level_choice = input("Select level: ").strip()  # read input
    levels = {'1': 'easy', '2': 'medium', '3': 'hard'}  # mapping from numeric selection
    level = levels.get(level_choice, 'easy')  # default to 'easy' if invalid
    
    # Get question data  # prompt for question fields
    print("\nEnter question details:")  # instruction
    question_text = input("Question: ")  # read question text
    option_a = input("Option A: ")  # read option A
    option_b = input("Option B: ")  # read option B
    option_c = input("Option C: ")  # read option C
    option_d = input("Option D: ")  # read option D
    correct = input("Correct answer (A/B/C/D): ").upper()  # read and normalize correct answer
    explanation = input("Explanation (optional): ")  # read optional explanation
    
    # Create question  # save new Question instance to DB
    Question.objects.create(
        subject=subject,  # FK relation
        question_text=question_text,  # question body
        option_a=option_a,  # option A
        option_b=option_b,  # option B
        option_c=option_c,  # option C
        option_d=option_d,  # option D
        correct_answer=correct,  # correct option
        level=level,  # difficulty level
        explanation=explanation  # optional explanation
    )
    
    print("\n✅ Question added successfully!")  # confirmation message


def update_question():  # interactive update function for existing question
    """Update an existing question"""  # docstring
    print("\n" + "=" * 80)  # header separator
    print("UPDATE QUESTION")  # header
    print("=" * 80)  # separator
    
    question_id = input("\nEnter question ID: ").strip()  # read question id from user
    
    try:
        question = Question.objects.get(id=question_id)  # fetch question by id
        
        print(f"\nCurrent question:")  # show current values
        print(f"Question: {question.question_text}")  # show full question text
        print(f"A) {question.option_a}")  # option A
        print(f"B) {question.option_b}")  # option B
        print(f"C) {question.option_c}")  # option C
        print(f"D) {question.option_d}")  # option D
        print(f"Correct: {question.correct_answer}")  # correct option
        
        print("\nEnter new values (press Enter to keep current):")  # prompt for updates
        
        new_text = input(f"Question [{question.question_text[:50]}...]: ")  # input for new text
        if new_text:  # if provided
            question.question_text = new_text  # update field
        
        new_a = input(f"Option A [{question.option_a[:30]}...]: ")  # input option A
        if new_a:
            question.option_a = new_a  # update
        
        new_b = input(f"Option B [{question.option_b[:30]}...]: ")  # input option B
        if new_b:
            question.option_b = new_b  # update
        
        new_c = input(f"Option C [{question.option_c[:30]}...]: ")  # input option C
        if new_c:
            question.option_c = new_c  # update
        
        new_d = input(f"Option D [{question.option_d[:30]}...]: ")  # input option D
        if new_d:
            question.option_d = new_d  # update
        
        new_correct = input(f"Correct answer [{question.correct_answer}]: ").upper()  # input correct answer
        if new_correct:
            question.correct_answer = new_correct  # update
        
        new_explanation = input(f"Explanation: ")  # input explanation
        if new_explanation:
            question.explanation = new_explanation  # update
        
        question.save()  # save changes to DB
        print("\n✅ Question updated successfully!")  # confirmation
        
    except Question.DoesNotExist:  # handle missing question
        print(f"\n❌ Question ID {question_id} not found!")  # error message


def delete_question():  # interactive delete function
    """Delete a question"""  # docstring
    print("\n" + "=" * 80)  # header
    print("DELETE QUESTION")  # header text
    print("=" * 80)  # separator
    
    question_id = input("\nEnter question ID: ").strip()  # read id
    
    try:
        question = Question.objects.get(id=question_id)  # fetch question
        print(f"\nQuestion: {question.question_text[:80]}...")  # show preview of question
        
        confirm = input("Are you sure you want to delete this? (yes/no): ").lower()  # confirm deletion
        if confirm == 'yes':
            question.delete()  # delete record from DB
            print("\n✅ Question deleted successfully!")  # confirmation
        else:
            print("\n❌ Deletion cancelled")  # cancelled message
            
    except Question.DoesNotExist:  # handle not found
        print(f"\n❌ Question ID {question_id} not found!")  # error message


def show_menu():  # show the interactive menu options
    """Show main menu"""  # docstring
    print("\n" + "=" * 80)  # visual separator
    print("📝 QUESTION MANAGER (No Admin Needed!)")  # title line
    print("=" * 80)  # separator
    print("\n1. List all subjects")  # menu option 1
    print("2. List questions (by subject & level)")  # menu option 2
    print("3. Add new question")  # menu option 3
    print("4. Update question")  # menu option 4
    print("5. Delete question")  # menu option 5
    print("6. Exit")  # menu option 6


def main():  # main interactive loop
    """Main function"""  # docstring
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       📝 QUESTION MANAGER                                    ║
║                                                                              ║
║  Manage questions directly in database - No admin panel needed!             ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)  # ASCII banner printed at start
    
    while True:  # loop until user exits
        show_menu()  # display menu
        choice = input("\n👉 Enter your choice (1-6): ").strip()  # read user choice
        
        if choice == '1':  # list subjects
            list_subjects()  # call function
            input("\nPress Enter to continue...")  # wait for user
        
        elif choice == '2':  # list questions
            subject_code = input("\nEnter subject code (e.g., CSW351-AI): ").strip().upper()  # read subject code
            level = input("Enter level (easy/medium/hard): ").strip().lower()  # read level
            list_questions(subject_code, level)  # call listing function
            input("\nPress Enter to continue...")  # pause
        
        elif choice == '3':  # add question
            add_question()  # call interactive add
            input("\nPress Enter to continue...")  # pause
        
        elif choice == '4':  # update question
            update_question()  # call update flow
            input("\nPress Enter to continue...")  # pause
        
        elif choice == '5':  # delete question
            delete_question()  # call delete flow
            input("\nPress Enter to continue...")  # pause
        
        elif choice == '6':  # exit option
            print("\n👋 Goodbye!")  # goodbye message
            break  # exit loop
        
        else:  # invalid choice
            print("\n❌ Invalid choice!")  # show error


if __name__ == '__main__':  # run main when executed as script
    try:
        main()  # start interactive loop
    except KeyboardInterrupt:  # handle Ctrl-C gracefully
        print("\n\n👋 Interrupted by user. Goodbye!")  # friendly message
    except Exception as e:  # catch all other exceptions and print traceback
        print(f"\n❌ Error: {e}")  # print error message
        import traceback  # import traceback for detailed error
        traceback.print_exc()  # print stack trace

