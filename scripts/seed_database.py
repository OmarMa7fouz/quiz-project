"""
Seed script to populate the database with sample data
Run this script with: python manage.py shell < scripts/seed_database.py
Or: python scripts/seed_database.py (if configured properly)
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_quiz_project.settings')
django.setup()

from django.contrib.auth.models import User
from apps.quiz_app.models import Category, Quiz, Question, Answer


def create_superuser():
    """Create a superuser if it doesn't exist"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print('✓ Superuser created: username=admin, password=admin123')
    else:
        print('✓ Superuser already exists')


def create_categories():
    """Create sample categories"""
    categories_data = [
        {'name': 'البرمجة', 'slug': 'programming', 'description': 'أسئلة عن البرمجة وأساسياتها', 'icon': 'bi-code-slash'},
        {'name': 'قواعد البيانات', 'slug': 'database', 'description': 'أسئلة عن قواعد البيانات وSQL', 'icon': 'bi-database'},
        {'name': 'تطوير الويب', 'slug': 'web-development', 'description': 'أسئلة عن HTML, CSS, JavaScript', 'icon': 'bi-globe'},
        {'name': 'الذكاء الاصطناعي', 'slug': 'ai', 'description': 'أسئلة عن الذكاء الاصطناعي وتعلم الآلة', 'icon': 'bi-robot'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f'✓ Category created: {category.name}')
    
    return Category.objects.all()


def create_quizzes(categories):
    """Create sample quizzes"""
    admin_user = User.objects.get(username='admin')
    programming_category = categories.get(slug='programming')
    web_category = categories.get(slug='web-development')
    
    quizzes_data = [
        {
            'title': 'أساسيات Python',
            'slug': 'python-basics',
            'description': 'اختبار شامل لأساسيات لغة Python',
            'category': programming_category,
            'difficulty': 'easy',
            'duration': 30,
            'pass_percentage': 70,
        },
        {
            'title': 'Django المتقدم',
            'slug': 'django-advanced',
            'description': 'اختبار متقدم في إطار عمل Django',
            'category': programming_category,
            'difficulty': 'hard',
            'duration': 45,
            'pass_percentage': 60,
        },
        {
            'title': 'HTML & CSS',
            'slug': 'html-css',
            'description': 'اختبار في HTML و CSS للمبتدئين',
            'category': web_category,
            'difficulty': 'easy',
            'duration': 25,
            'pass_percentage': 70,
        },
    ]
    
    created_quizzes = []
    for quiz_data in quizzes_data:
        quiz, created = Quiz.objects.get_or_create(
            slug=quiz_data['slug'],
            defaults={**quiz_data, 'created_by': admin_user}
        )
        if created:
            print(f'✓ Quiz created: {quiz.title}')
        created_quizzes.append(quiz)
    
    return created_quizzes


def create_questions(quizzes):
    """Create sample questions for quizzes"""
    
    # Python basics quiz questions
    python_quiz = quizzes[0]
    
    python_questions = [
        {
            'question_text': 'ما هي لغة البرمجة التي تستخدم Django؟',
            'code_snippet': None,
            'question_type': 'single',
            'points': 1,
            'order': 1,
            'answers': [
                {'text': 'JavaScript', 'is_correct': False},
                {'text': 'Python', 'is_correct': True},
                {'text': 'Java', 'is_correct': False},
                {'text': 'PHP', 'is_correct': False},
            ]
        },
        {
            'question_text': 'ما هو ناتج الكود التالي؟',
            'code_snippet': 'x = 5\ny = 3\nprint(x + y)',
            'question_type': 'single',
            'points': 2,
            'order': 2,
            'answers': [
                {'text': '8', 'is_correct': True},
                {'text': '53', 'is_correct': False},
                {'text': 'Error', 'is_correct': False},
                {'text': '15', 'is_correct': False},
            ]
        },
        {
            'question_text': 'أي من الآتي يستخدم لإنشاء قائمة (list) في Python؟',
            'code_snippet': None,
            'question_type': 'single',
            'points': 1,
            'order': 3,
            'answers': [
                {'text': '[]', 'is_correct': True},
                {'text': '{}', 'is_correct': False},
                {'text': '()', 'is_correct': False},
                {'text': '<>', 'is_correct': False},
            ]
        },
        {
            'question_text': 'Python هي لغة برمجة مفسرة (interpreted)',
            'code_snippet': None,
            'question_type': 'true_false',
            'points': 1,
            'order': 4,
            'answers': [
                {'text': 'صح', 'is_correct': True},
                {'text': 'خطأ', 'is_correct': False},
            ]
        },
        {
            'question_text': 'ما هي الدالة المستخدمة لطباعة النص في Python؟',
            'code_snippet': None,
            'question_type': 'single',
            'points': 1,
            'order': 5,
            'answers': [
                {'text': 'echo()', 'is_correct': False},
                {'text': 'printf()', 'is_correct': False},
                {'text': 'print()', 'is_correct': True},
                {'text': 'console.log()', 'is_correct': False},
            ]
        },
    ]
    
    for q_data in python_questions:
        answers_data = q_data.pop('answers')
        question, created = Question.objects.get_or_create(
            quiz=python_quiz,
            question_text=q_data['question_text'],
            defaults=q_data
        )
        
        if created:
            for idx, ans_data in enumerate(answers_data):
                Answer.objects.create(
                    question=question,
                    answer_text=ans_data['text'],
                    is_correct=ans_data['is_correct'],
                    order=idx
                )
            print(f'✓ Question created: {question.question_text[:50]}...')
    
    # Django advanced quiz questions
    django_quiz = quizzes[1]
    
    django_questions = [
        {
            'question_text': 'ما هو ORM في Django؟',
            'code_snippet': None,
            'question_type': 'single',
            'points': 2,
            'order': 1,
            'answers': [
                {'text': 'Object-Relational Mapping', 'is_correct': True},
                {'text': 'Object-Request Manager', 'is_correct': False},
                {'text': 'Online Resource Manager', 'is_correct': False},
                {'text': 'Operational Response Module', 'is_correct': False},
            ]
        },
        {
            'question_text': 'ما هو الأمر المستخدم لإنشاء migrations في Django؟',
            'code_snippet': None,
            'question_type': 'single',
            'points': 1,
            'order': 2,
            'answers': [
                {'text': 'python manage.py migrate', 'is_correct': False},
                {'text': 'python manage.py makemigrations', 'is_correct': True},
                {'text': 'python manage.py createmigrations', 'is_correct': False},
                {'text': 'python manage.py migration', 'is_correct': False},
            ]
        },
    ]
    
    for q_data in django_questions:
        answers_data = q_data.pop('answers')
        question, created = Question.objects.get_or_create(
            quiz=django_quiz,
            question_text=q_data['question_text'],
            defaults=q_data
        )
        
        if created:
            for idx, ans_data in enumerate(answers_data):
                Answer.objects.create(
                    question=question,
                    answer_text=ans_data['text'],
                    is_correct=ans_data['is_correct'],
                    order=idx
                )
            print(f'✓ Question created: {question.question_text[:50]}...')
    
    # HTML & CSS quiz questions
    html_quiz = quizzes[2]
    
    html_questions = [
        {
            'question_text': 'ما هو الوسم المستخدم لإنشاء رابط في HTML؟',
            'code_snippet': None,
            'question_type': 'single',
            'points': 1,
            'order': 1,
            'answers': [
                {'text': '<link>', 'is_correct': False},
                {'text': '<a>', 'is_correct': True},
                {'text': '<href>', 'is_correct': False},
                {'text': '<url>', 'is_correct': False},
            ]
        },
        {
            'question_text': 'CSS تعني Cascading Style Sheets',
            'code_snippet': None,
            'question_type': 'true_false',
            'points': 1,
            'order': 2,
            'answers': [
                {'text': 'صح', 'is_correct': True},
                {'text': 'خطأ', 'is_correct': False},
            ]
        },
    ]
    
    for q_data in html_questions:
        answers_data = q_data.pop('answers')
        question, created = Question.objects.get_or_create(
            quiz=html_quiz,
            question_text=q_data['question_text'],
            defaults=q_data
        )
        
        if created:
            for idx, ans_data in enumerate(answers_data):
                Answer.objects.create(
                    question=question,
                    answer_text=ans_data['text'],
                    is_correct=ans_data['is_correct'],
                    order=idx
                )
            print(f'✓ Question created: {question.question_text[:50]}...')


def main():
    """Main function to seed the database"""
    print('\n🌱 Starting database seeding...\n')
    
    print('Step 1: Creating superuser...')
    create_superuser()
    
    print('\nStep 2: Creating categories...')
    categories = create_categories()
    
    print('\nStep 3: Creating quizzes...')
    quizzes = create_quizzes(categories)
    
    print('\nStep 4: Creating questions and answers...')
    create_questions(quizzes)
    
    print('\n✅ Database seeding completed successfully!')
    print('\nYou can now:')
    print('1. Run the server: python manage.py runserver')
    print('2. Login to admin: http://127.0.0.1:8000/admin/')
    print('   Username: admin')
    print('   Password: admin123')
    print('3. Visit the site: http://127.0.0.1:8000/\n')


if __name__ == '__main__':
    main()

