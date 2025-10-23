"""
Chatbot Web Views
==================

Django views for web-based chatbot interface.
Simplified chatbot for subject and difficulty selection.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Subject, Question, get_random_questions, get_all_subjects


def chatbot_home(request):
    """Chatbot home page"""
    # Clear any existing session data
    request.session.pop('selected_subject', None)
    request.session.pop('selected_level', None)
    
    context = {
        'title': 'Quiz Chatbot'
    }
    return render(request, 'chatbot/home.html', context)


def chatbot_select_subject(request):
    """Select subject via chatbot"""
    subjects = get_all_subjects()
    
    context = {
        'subjects': subjects,
        'title': 'Select Subject'
    }
    return render(request, 'chatbot/select_subject.html', context)


def chatbot_select_difficulty(request):
    """Select difficulty level"""
    subject_code = request.GET.get('subject')
    
    if not subject_code:
        return redirect('quiz:chatbot_select_subject')
    
    try:
        subject = Subject.objects.get(code=subject_code)
    except Subject.DoesNotExist:
        return render(request, 'chatbot/error.html', {
            'error': f'Subject {subject_code} not found'
        })
    
    # Store subject in session
    request.session['selected_subject'] = subject_code
    
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
        'title': f'Select Difficulty - {subject.name}'
    }
    return render(request, 'chatbot/select_difficulty.html', context)


def chatbot_start_quiz(request):
    """Start quiz via chatbot - redirect to quiz page"""
    subject_code = request.session.get('selected_subject')
    level = request.GET.get('level', 'easy')
    
    if not subject_code:
        return redirect('quiz:chatbot_select_subject')
    
    # Store level in session
    request.session['selected_level'] = level
    
    # Redirect to quiz
    return redirect('quiz:take_quiz', subject_code=subject_code, level=level)
