from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from .models import Subject, Question, get_random_questions, get_all_subjects, get_subject_levels


def home(request):
    """Home page - Select subject"""
    subjects = get_all_subjects()
    
    context = {
        'subjects': subjects,
        'total_subjects': subjects.count(),
    }
    return render(request, 'home.html', context)


def select_difficulty(request, subject_code):
    """Select difficulty level for the chosen subject"""
    subject = get_object_or_404(Subject, code=subject_code)
    available_levels = get_subject_levels(subject_code)
    
    # Count questions per level
    levels_data = []
    for level in ['easy', 'medium', 'hard']:
        count = subject.questions_by_level(level).count()
        if count > 0:
            levels_data.append({
                'level': level,
                'display': level.title(),
                'count': count
            })
    
    context = {
        'subject': subject,
        'levels': levels_data,
    }
    return render(request, 'select_difficulty.html', context)


def take_quiz(request, subject_code, level):
    """
    Display random quiz questions (10 questions)
    No login required, no saving results
    """
    subject = get_object_or_404(Subject, code=subject_code)
    
    # Get 10 random questions
    questions = get_random_questions(subject_code, level, num_questions=10)
    
    if not questions:
        context = {
            'error': True,
            'message': f'No questions available for {subject.name} - {level.title()} level.'
        }
        return render(request, 'quiz.html', context)
    
    context = {
        'subject': subject,
        'level': level.title(),
        'questions': questions,
        'total_questions': len(questions),
    }
    return render(request, 'quiz.html', context)


def check_answers(request):
    """
    Check answers via AJAX
    Returns immediate feedback without saving to database
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    # Get submitted answers
    import json
    data = json.loads(request.body)
    answers = data.get('answers', {})
    
    # Check each answer
    results = []
    correct_count = 0
    
    for question_id, selected_option in answers.items():
        try:
            question = Question.objects.get(id=question_id)
            is_correct = question.check_answer(selected_option)
            
            if is_correct:
                correct_count += 1
            
            results.append({
                'question_id': question_id,
                'selected': selected_option,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
                'explanation': question.explanation,
            })
        except Question.DoesNotExist:
            continue
    
    total_questions = len(answers)
    percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    response_data = {
        'success': True,
        'correct_count': correct_count,
        'total_questions': total_questions,
        'percentage': round(percentage, 2),
        'results': results,
    }
    
    return JsonResponse(response_data)


def check_answers(request):
    """Check quiz answers and return results"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        answers = data.get('answers', {})
        
        results = []
        correct_count = 0
        
        for question_id, selected_answer in answers.items():
            try:
                question = Question.objects.get(id=int(question_id))
                is_correct = selected_answer == question.correct_answer
                
                if is_correct:
                    correct_count += 1
                
                results.append({
                    'question_id': question_id,
                    'selected': selected_answer,
                    'correct_answer': question.correct_answer,
                    'is_correct': is_correct
                })
                
            except Question.DoesNotExist:
                return JsonResponse({'error': f'Question {question_id} not found'}, status=404)
        
        total_questions = len(results)
        percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        response_data = {
            'total_questions': total_questions,
            'correct_count': correct_count,
            'incorrect_count': total_questions - correct_count,
            'percentage': round(percentage, 2),
            'results': results
        }
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def quiz_list(request):
    """List all subjects with their available levels"""
    subjects = get_all_subjects()
    
    subjects_data = []
    for subject in subjects:
        levels_info = []
        for level in ['easy', 'medium', 'hard']:
            count = subject.questions_by_level(level).count()
            if count > 0:
                levels_info.append({
                    'level': level,
                    'count': count
                })
        
        subjects_data.append({
            'subject': subject,
            'levels': levels_info,
            'total_questions': subject.total_questions()
        })
    
    context = {
        'subjects_data': subjects_data,
    }
    return render(request, 'quiz_list.html', context)
