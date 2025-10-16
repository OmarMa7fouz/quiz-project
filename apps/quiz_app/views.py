from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Quiz, Question, Answer, QuizResult, UserAnswer, Category


def home(request):
    """Home page view"""
    context = {
        'total_quizzes': Quiz.objects.filter(is_active=True).count(),
        'categories': Category.objects.all()[:4],
        'featured_quizzes': Quiz.objects.filter(is_active=True)[:3],
    }
    return render(request, 'home.html', context)


def quiz_list(request):
    """List only the 4 main subjects with their difficulty levels"""
    # Define the 4 main subjects with their actual database titles
    main_subjects = {
        'CSW351-AI': 'CSW351',
        'INT353-MULTIMEDIA': 'INT353', 
        'INT341-WEB TECHNOLOGY': 'INT341-WEB TECHNOLOGY',
        'CSW325-PARALLEL PROCESSING': 'CSW325-PARALLEL PROCESSING'
    }
    
    # Get all quiz titles that match our subjects
    quiz_titles = []
    for display_name, db_name in main_subjects.items():
        quiz_titles.extend([f"{db_name} - EASY", f"{db_name} - MEDIUM", f"{db_name} - HARD"])
    
    # Get quizzes for these subjects only
    quizzes = Quiz.objects.filter(
        is_active=True,
        title__in=quiz_titles
    ).select_related('category').order_by('title')
    
    # Organize by subject
    subjects_data = {}
    for display_name in main_subjects.keys():
        subjects_data[display_name] = {
            'easy': None,
            'medium': None,
            'hard': None
        }
    
    # Populate the data
    for quiz in quizzes:
        for display_name, db_name in main_subjects.items():
            if quiz.title.startswith(db_name):
                difficulty = quiz.title.split(' - ')[-1].lower()
                subjects_data[display_name][difficulty] = quiz
                break
    
    # Filter by subject if requested
    selected_subject = request.GET.get('subject')
    if selected_subject and selected_subject in main_subjects.keys():
        filtered_data = {selected_subject: subjects_data[selected_subject]}
        subjects_data = filtered_data
    
    # Filter by difficulty if requested
    selected_difficulty = request.GET.get('difficulty')
    if selected_difficulty:
        filtered_data = {}
        for subject, levels in subjects_data.items():
            filtered_levels = {}
            if selected_difficulty in levels and levels[selected_difficulty]:
                filtered_levels[selected_difficulty] = levels[selected_difficulty]
            if filtered_levels:
                filtered_data[subject] = filtered_levels
        subjects_data = filtered_data
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        filtered_data = {}
        for subject, levels in subjects_data.items():
            if search_query.lower() in subject.lower():
                filtered_data[subject] = levels
        subjects_data = filtered_data
    
    context = {
        'subjects_data': subjects_data,
        'main_subjects': list(main_subjects.keys()),
    }
    return render(request, 'quiz_list.html', context)


@login_required
def take_quiz(request, quiz_id):
    """Take a quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    questions = quiz.questions.prefetch_related('answers').all()
    
    # Create a new quiz result
    quiz_result = QuizResult.objects.create(
        user=request.user,
        quiz=quiz,
        total_points=sum(q.points for q in questions)
    )
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'quiz_result_id': quiz_result.id,
    }
    return render(request, 'quiz.html', context)


@login_required
def submit_quiz(request, quiz_id):
    """Submit quiz answers"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_result_id = request.POST.get('quiz_result_id')
    quiz_result = get_object_or_404(QuizResult, id=quiz_result_id, user=request.user)
    
    # Process answers
    total_score = 0
    questions = quiz.questions.all()
    
    for question in questions:
        answer_id = request.POST.get(f'question_{question.id}')
        if answer_id:
            selected_answer = get_object_or_404(Answer, id=answer_id)
            is_correct = selected_answer.is_correct
            points = question.points if is_correct else 0
            
            UserAnswer.objects.create(
                quiz_result=quiz_result,
                question=question,
                selected_answer=selected_answer,
                is_correct=is_correct,
                points_earned=points
            )
            
            total_score += points
    
    # Update quiz result
    quiz_result.score = total_score
    quiz_result.percentage = (total_score / quiz_result.total_points) * 100 if quiz_result.total_points > 0 else 0
    quiz_result.passed = quiz_result.percentage >= quiz.pass_percentage
    quiz_result.completed = True
    quiz_result.completed_at = timezone.now()
    quiz_result.time_taken = int(request.POST.get('time_taken', 0))
    quiz_result.save()
    
    return redirect('quiz:view_results', result_id=quiz_result.id)


@login_required
def view_results(request, result_id):
    """View quiz results"""
    result = get_object_or_404(QuizResult, id=result_id, user=request.user)
    user_answers = result.user_answers.select_related('question', 'selected_answer').all()
    
    # Prepare data for charts
    categories_performance = {}
    for answer in user_answers:
        category = answer.question.quiz.category.name
        if category not in categories_performance:
            categories_performance[category] = {'correct': 0, 'total': 0}
        categories_performance[category]['total'] += 1
        if answer.is_correct:
            categories_performance[category]['correct'] += 1
    
    # Calculate category scores
    category_labels = []
    category_scores = []
    for category, data in categories_performance.items():
        category_labels.append(category)
        score = (data['correct'] / data['total']) * 100 if data['total'] > 0 else 0
        category_scores.append(round(score, 2))
    
    context = {
        'result': result,
        'user_answers': user_answers,
        'categories': category_labels,
        'category_scores': category_scores,
    }
    return render(request, 'results.html', context)
