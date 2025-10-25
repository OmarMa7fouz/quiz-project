"""
🗄️ QUIZ DATABASE MANAGER
==========================

This file handles ALL database operations:
- Seeding (creating initial data)
- Querying (fetching and randomizing questions)
- Viewing (checking database contents)

SUBJECTS: CSW351-AI, INT353-MULTIMEDIA, INT341-WEB TECHNOLOGY, CSW325-PARALLEL PROCESSING
LEVELS: easy, medium, hard
QUESTIONS: 30 per level (shows 10 random)

Run with: python quiz_database.py
"""

import os
import sys
import django
import random

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_quiz_project.settings')
django.setup()

from django.contrib.auth.models import User
from apps.quiz_app.models import Category, Quiz, Question, Answer, QuizResult, UserAnswer


# ============================================================================
# 📚 CONFIGURATION
# ============================================================================

SUBJECTS = {
    'CSW351-AI': {
        'name': 'Artificial Intelligence',
        'description': 'AI concepts, algorithms, and applications',
        'icon': 'bi-robot'
    },
    'INT353-MULTIMEDIA': {
        'name': 'Multimedia',
        'description': 'Multimedia systems, graphics, audio, video',
        'icon': 'bi-film'
    },
    'INT341-WEB TECHNOLOGY': {
        'name': 'Web Technology',
        'description': 'Web development, HTML, CSS, JavaScript',
        'icon': 'bi-globe'
    },
    'CSW325-PARALLEL PROCESSING': {
        'name': 'Parallel Processing',
        'description': 'Parallel computing, multi-threading, distributed systems',
        'icon': 'bi-cpu'
    }
}

DIFFICULTY_LEVELS = ['easy', 'medium', 'hard']
QUESTIONS_PER_LEVEL = 30
QUESTIONS_TO_SHOW = 10


# ============================================================================
# 🌱 DATABASE SEEDING FUNCTIONS
# ============================================================================

# create_chatbot_user: ensure a 'chatbot' user exists and return the User instance
def create_chatbot_user():
    """Create chatbot user if doesn't exist"""
    if not User.objects.filter(username='chatbot').exists():
        User.objects.create_user(
            username='chatbot',
            email='chatbot@quiz.com',
            password='chatbot123'
        )
        print('✅ Chatbot user created: chatbot / chatbot123')
    else:
        print('✅ Chatbot user exists')
    return User.objects.get(username='chatbot')


def seed_database(clear_existing=False):
    """
    Seed database with subjects, quizzes, and placeholder questions
    
    Args:
        clear_existing (bool): If True, clear all existing data first
    """
    # seed_database: populate DB with categories, quizzes and placeholder questions
    # clear_existing controls whether to wipe existing quiz-related tables first
    print('\n' + '='*80)
    print('🌱 SEEDING DATABASE')
    print('='*80)
    
    if clear_existing:
        print('\n⚠️  Clearing existing data...')
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Quiz.objects.all().delete()
        Category.objects.all().delete()
        print('✅ Existing data cleared')
    
    admin = create_chatbot_user()
    
    total_quizzes = 0
    total_questions = 0
    
    for subject_code, subject_info in SUBJECTS.items():
        # Create category
        category, created = Category.objects.get_or_create(
            slug=subject_code.lower(),
            defaults={
                'name': subject_code,
                'description': subject_info['description'],
                'icon': subject_info['icon']
            }
        )
        
        if created:
            print(f'\n✅ Created subject: {subject_code}')
        else:
            print(f'\n♻️  Subject exists: {subject_code}')
        
        # Create quizzes for each difficulty level
        for level in DIFFICULTY_LEVELS:
            quiz_slug = f"{subject_code.lower()}-{level}"
            
            quiz, created = Quiz.objects.get_or_create(
                slug=quiz_slug,
                defaults={
                    'title': f'{subject_code} - {level.upper()}',
                    'description': f'{subject_info["name"]} quiz - {level} level',
                    'category': category,
                    'difficulty': level,
                    'duration': 15 if level == 'easy' else (20 if level == 'medium' else 25),
                    'pass_percentage': 70 if level == 'easy' else (65 if level == 'medium' else 60),
                    'is_active': True,
                    'created_by': admin
                }
            )
            
            if created:
                total_quizzes += 1
                print(f'   ✅ {level.upper()}: Creating {QUESTIONS_PER_LEVEL} placeholder questions...')
                
                # Create placeholder questions
                for q_num in range(1, QUESTIONS_PER_LEVEL + 1):
                    question = Question.objects.create(
                        quiz=quiz,
                        question_text=f'[PLACEHOLDER] {subject_code} - {level.upper()} - Q{q_num}: Add your question here',
                        code_snippet=None,
                        question_type='single',
                        points=1,
                        order=q_num,
                        explanation=f'Add explanation for question {q_num}'
                    )
                    
                    total_questions += 1
                    
                    # Create 4 answer options
                    Answer.objects.create(
                        question=question,
                        answer_text=f'[Option A] Replace with real answer',
                        is_correct=True,
                        order=0
                    )
                    Answer.objects.create(
                        question=question,
                        answer_text=f'[Option B] Replace with real answer',
                        is_correct=False,
                        order=1
                    )
                    Answer.objects.create(
                        question=question,
                        answer_text=f'[Option C] Replace with real answer',
                        is_correct=False,
                        order=2
                    )
                    Answer.objects.create(
                        question=question,
                        answer_text=f'[Option D] Replace with real answer',
                        is_correct=False,
                        order=3
                    )
            else:
                print(f'   ♻️  {level.upper()}: Already exists ({quiz.questions.count()} questions)')
    
    print('\n' + '='*80)
    print('✅ DATABASE SEEDING COMPLETED')
    print(f'   Created: {total_quizzes} quizzes, {total_questions} questions')
    print('='*80)


# ============================================================================
# 🔍 DATABASE QUERY FUNCTIONS
# ============================================================================

# get_all_subjects: return list of (name, description) for all Category objects
def get_all_subjects():
    """Get all available subjects"""
    categories = Category.objects.all()
    return [(cat.name, cat.description) for cat in categories]


# get_subject_by_code: lookup Category by its name and return first match or None
def get_subject_by_code(subject_code):
    """Get category by subject code"""
    return Category.objects.filter(name=subject_code).first()


# get_quiz: find a Quiz by subject_code and difficulty (slug-based lookup)
def get_quiz(subject_code, difficulty):
    """
    Get specific quiz by subject code and difficulty
    
    Args:
        subject_code (str): Subject code (e.g., 'CSW351-AI')
        difficulty (str): Difficulty level ('easy', 'medium', 'hard')
    
    Returns:
        Quiz object or None
    """
    slug = f"{subject_code.lower()}-{difficulty.lower()}"
    return Quiz.objects.filter(slug=slug).first()


# get_random_questions: return `count` randomized Question objects for a Quiz
def get_random_questions(quiz, count=QUESTIONS_TO_SHOW):
    """
    Get random questions from a quiz
    
    Args:
        quiz (Quiz): Quiz object
        count (int): Number of questions to return
    
    Returns:
        List of Question objects
    """
    all_questions = list(quiz.questions.prefetch_related('answers').all())
    
    if len(all_questions) == 0:
        return []
    
    # Select random questions
    num_questions = min(count, len(all_questions))
    selected_questions = random.sample(all_questions, num_questions)
    
    # Shuffle the selected questions
    random.shuffle(selected_questions)
    
    return selected_questions


# get_question_with_answers: return Question (with answers prefetched) or None
def get_question_with_answers(question_id):
    """Get a question with its answers"""
    try:
        question = Question.objects.prefetch_related('answers').get(id=question_id)
        return question
    except Question.DoesNotExist:
        return None


# check_answer: return True if the specified answer_id for question_id is_correct
def check_answer(question_id, answer_id):
    """
    Check if an answer is correct
    
    Args:
        question_id (int): Question ID
        answer_id (int): Answer ID
    
    Returns:
        bool: True if correct, False otherwise
    """
    try:
        answer = Answer.objects.get(id=answer_id, question_id=question_id)
        return answer.is_correct
    except Answer.DoesNotExist:
        return False


# get_correct_answer: fetch the Answer object marked correct for a question, or None
def get_correct_answer(question_id):
    """Get the correct answer for a question"""
    try:
        question = Question.objects.get(id=question_id)
        correct_answer = question.answers.filter(is_correct=True).first()
        return correct_answer
    except Question.DoesNotExist:
        return None


# save_quiz_result: compute score, create QuizResult and related UserAnswer rows
def save_quiz_result(user, quiz, questions, user_answers):
    """
    Save quiz result to database
    
    Args:
        user (User): User object
        quiz (Quiz): Quiz object
        questions (list): List of Question objects
        user_answers (dict): Dict of {question_id: answer_id}
    
    Returns:
        QuizResult object
    """
    # Calculate score
    correct_count = 0
    total_points = 0
    
    for question in questions:
        total_points += question.points
        if user_answers.get(question.id):
            answer_id = user_answers[question.id]
            if check_answer(question.id, answer_id):
                correct_count += 1
    
    percentage = (correct_count / len(questions)) * 100 if questions else 0
    
    # Create quiz result
    quiz_result = QuizResult.objects.create(
        user=user,
        quiz=quiz,
        score=correct_count,
        total_points=total_points,
        percentage=percentage,
        passed=percentage >= quiz.pass_percentage,
        completed=True
    )
    
    # Save individual answers
    for question in questions:
        if user_answers.get(question.id):
            answer_id = user_answers[question.id]
            is_correct = check_answer(question.id, answer_id)
            
            try:
                selected_answer = Answer.objects.get(id=answer_id)
                UserAnswer.objects.create(
                    quiz_result=quiz_result,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=is_correct,
                    points_earned=question.points if is_correct else 0
                )
            except Answer.DoesNotExist:
                pass
    
    return quiz_result


# get_user_results: return recent QuizResult rows for a user (limit default 10)
def get_user_results(user, limit=10):
    """Get user's quiz results"""
    return QuizResult.objects.filter(user=user).order_by('-started_at')[:limit]


# ============================================================================
# 👁️ DATABASE VIEWER FUNCTIONS
# ============================================================================

# view_database_summary: print counts and summaries for categories, quizzes, questions, answers and results
def view_database_summary():
    """View complete database summary"""
    print('\n' + '='*80)
    print('📊 DATABASE SUMMARY')
    print('='*80)
    
    print(f'\n📚 Total Subjects: {Category.objects.count()}')
    for cat in Category.objects.all():
        print(f'   • {cat.name}: {cat.description}')
    
    print(f'\n📝 Total Quizzes: {Quiz.objects.count()}')
    for subject_code in SUBJECTS.keys():
        subject_quizzes = Quiz.objects.filter(category__name=subject_code)
        print(f'   • {subject_code}: {subject_quizzes.count()} quizzes')
        for quiz in subject_quizzes:
            print(f'      - {quiz.difficulty.upper()}: {quiz.questions.count()} questions')
    
    print(f'\n❓ Total Questions: {Question.objects.count()}')
    print(f'✅ Total Answers: {Answer.objects.count()}')
    print(f'👥 Total Users: {User.objects.count()}')
    print(f'📈 Total Quiz Results: {QuizResult.objects.count()}')
    
    print('\n' + '='*80)


# view_all_quizzes: print a summary for each subject and difficulty level if a quiz exists
def view_all_quizzes():
    """View all available quizzes"""
    print('\n' + '='*80)
    print('📚 ALL AVAILABLE QUIZZES')
    print('='*80)
    
    for subject_code in SUBJECTS.keys():
        print(f'\n{subject_code}: {SUBJECTS[subject_code]["name"]}')
        for level in DIFFICULTY_LEVELS:
            quiz = get_quiz(subject_code, level)
            if quiz:
                q_count = quiz.questions.count()
                print(f'   • {level.upper()}: {q_count} questions | '
                      f'{quiz.duration} min | '
                      f'Pass: {quiz.pass_percentage}%')
    
    print('\n' + '='*80)


 # view_quiz_details: display detailed metadata and a few sample questions for a quiz
def view_quiz_details(subject_code, difficulty):
    quiz = get_quiz(subject_code, difficulty)
    
    if not quiz:
        print(f'\n❌ Quiz not found: {subject_code} - {difficulty}')
        return
    
    print('\n' + '='*80)
    print(f'📝 QUIZ: {quiz.title}')
    print('='*80)
    
    print(f'\nSubject: {quiz.category.name}')
    print(f'Difficulty: {quiz.difficulty}')
    print(f'Duration: {quiz.duration} minutes')
    print(f'Pass Percentage: {quiz.pass_percentage}%')
    print(f'Total Questions: {quiz.questions.count()}')
    print(f'Questions Shown: {QUESTIONS_TO_SHOW}')
    
    print('\n📋 Sample Questions (first 3):')
    questions = quiz.questions.all()[:3]
    for i, q in enumerate(questions, 1):
        print(f'\n{i}. {q.question_text}')
        for ans in q.answers.all():
            mark = '✓' if ans.is_correct else '○'
            print(f'   {mark} {ans.answer_text}')
    
    print('\n' + '='*80)


# view_quiz_statistics: compute and print overall quiz attempt statistics and averages
def view_quiz_statistics():
    """View quiz statistics"""
    print('\n' + '='*80)
    print('📊 QUIZ STATISTICS')
    print('='*80)
    
    total_attempts = QuizResult.objects.filter(completed=True).count()
    passed_attempts = QuizResult.objects.filter(passed=True).count()
    
    print(f'\n📈 Total Attempts: {total_attempts}')
    print(f'✅ Passed: {passed_attempts}')
    print(f'❌ Failed: {total_attempts - passed_attempts}')
    
    if total_attempts > 0:
        pass_rate = (passed_attempts / total_attempts) * 100
        print(f'📊 Pass Rate: {pass_rate:.2f}%')
        
        avg_score = QuizResult.objects.filter(completed=True).aggregate(
            avg_score=django.db.models.Avg('percentage')
        )['avg_score']
        print(f'📊 Average Score: {avg_score:.2f}%')
    
    print('\n' + '='*80)


# ============================================================================
# 🎮 MAIN MENU FOR TESTING
# ============================================================================

def show_menu():
    """Show database manager menu"""
    print('\n' + '='*80)
    print('🗄️  QUIZ DATABASE MANAGER')
    print('='*80)
    print('\n1. 🌱 Seed Database (Create all quizzes and questions)')
    print('2. 🌱 Seed Database (Clear existing first)')
    print('3. 👁️  View Database Summary')
    print('4. 📋 View All Quizzes')
    print('5. 🔍 View Specific Quiz')
    print('6. 📊 View Statistics')
    print('7. ❌ Exit')


 # main: interactive menu loop to exercise database functions for testing
def main():
    """Main function for testing database operations"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        🗄️  QUIZ DATABASE MANAGER                            ║
║                                                                              ║
║  This file handles all database operations:                                  ║
║  ✅ Seeding database with quizzes and questions                             ║
║  ✅ Querying and fetching data                                              ║
║  ✅ Randomizing question selection                                          ║
║  ✅ Viewing database contents                                               ║
║                                                                              ║
║  Import this file in your chatbot to use the database functions!            ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        show_menu()
        
        choice = input('\n👉 Enter your choice (1-7): ').strip()
        
        if choice == '1':
            seed_database(clear_existing=False)
            input('\n✅ Press ENTER to continue...')
        
        elif choice == '2':
            confirm = input('\n⚠️  This will DELETE all existing data! Continue? (yes/no): ')
            if confirm.lower() == 'yes':
                seed_database(clear_existing=True)
            input('\n✅ Press ENTER to continue...')
        
        elif choice == '3':
            view_database_summary()
            input('\n👉 Press ENTER to continue...')
        
        elif choice == '4':
            view_all_quizzes()
            input('\n👉 Press ENTER to continue...')
        
        elif choice == '5':
            print('\n📚 Available Subjects:')
            for code in SUBJECTS.keys():
                print(f'   • {code}')
            subject = input('\nEnter subject code: ').strip().upper()
            
            print('\n📊 Levels: easy, medium, hard')
            level = input('Enter difficulty: ').strip().lower()
            
            view_quiz_details(subject, level)
            input('\n👉 Press ENTER to continue...')
        
        elif choice == '6':
            view_quiz_statistics()
            input('\n👉 Press ENTER to continue...')
        
        elif choice == '7':
            print('\n👋 Goodbye!')
            break
        
        else:
            print('\n❌ Invalid choice. Please try again.')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n👋 Interrupted by user. Goodbye!')
    except Exception as e:
        print(f'\n❌ Error: {e}')
        import traceback
        traceback.print_exc()

