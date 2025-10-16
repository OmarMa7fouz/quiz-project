"""
🤖 CHATBOT WEB VIEWS
=====================

Django views for web-based chatbot interface.
Handles all chatbot conversation flow in the browser.
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random

# Import database functions
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from quiz_database import (
    SUBJECTS,
    DIFFICULTY_LEVELS,
    get_quiz,
    get_random_questions,
    save_quiz_result,
    check_answer,
    get_correct_answer
)

from .models import Quiz, Question, Answer
from django.contrib.auth.models import User


# ============================================================================
# CHATBOT VIEWS
# ============================================================================

def chatbot_home(request):
    """Chatbot home page - start conversation"""
    # Clear any existing session data
    request.session.pop('chatbot_state', None)
    request.session.pop('chatbot_data', None)
    
    context = {
        'subjects': SUBJECTS,
        'page_title': 'Quiz Chatbot'
    }
    return render(request, 'chatbot/home.html', context)


def chatbot_select_subject(request):
    """Step 1: Select subject"""
    if request.method == 'POST':
        subject_code = request.POST.get('subject')
        
        if subject_code in SUBJECTS:
            # Store in session
            request.session['chatbot_data'] = {
                'subject': subject_code,
                'subject_name': SUBJECTS[subject_code]['name']
            }
            return redirect('quiz:chatbot_select_difficulty')
    
    context = {
        'subjects': SUBJECTS,
        'step': 1
    }
    return render(request, 'chatbot/select_subject.html', context)


def chatbot_select_difficulty(request):
    """Step 2: Select difficulty and redirect to quiz"""
    chatbot_data = request.session.get('chatbot_data', {})
    
    if not chatbot_data.get('subject'):
        return redirect('quiz:chatbot_select_subject')
    
    if request.method == 'POST':
        difficulty = request.POST.get('difficulty')
        
        if difficulty in DIFFICULTY_LEVELS:
            # Get quiz
            quiz = get_quiz(chatbot_data['subject'], difficulty)
            
            if not quiz:
                return render(request, 'chatbot/error.html', {
                    'error': 'Quiz not found. Please run database seeding first.'
                })
            
            # Clear chatbot session data
            request.session.pop('chatbot_data', None)
            
            # Redirect directly to the actual quiz page
            return redirect('quiz:take_quiz', quiz_id=quiz.id)
    
    context = {
        'subject': chatbot_data.get('subject'),
        'subject_name': chatbot_data.get('subject_name'),
        'levels': DIFFICULTY_LEVELS,
        'step': 2
    }
    return render(request, 'chatbot/select_difficulty.html', context)


def chatbot_load_quiz(request):
    """Step 3: Load quiz and redirect to actual quiz page"""
    chatbot_data = request.session.get('chatbot_data', {})
    
    if not chatbot_data.get('subject') or not chatbot_data.get('difficulty'):
        return redirect('quiz:chatbot_select_subject')
    
    # Get quiz
    quiz = get_quiz(chatbot_data['subject'], chatbot_data['difficulty'])
    
    if not quiz:
        return render(request, 'chatbot/error.html', {
            'error': 'Quiz not found. Please run database seeding first.'
        })
    
    # Clear chatbot session data
    request.session.pop('chatbot_data', None)
    
    # Redirect to the actual quiz page
    return redirect('quiz:take_quiz', quiz_id=quiz.id)


def chatbot_quiz(request):
    """Step 4: Conduct quiz - show questions one by one"""
    chatbot_data = request.session.get('chatbot_data', {})
    
    if not chatbot_data.get('questions'):
        return redirect('quiz:chatbot_select_subject')
    
    current_index = chatbot_data.get('current_question', 0)
    question_ids = chatbot_data.get('questions', [])
    
    # Check if quiz is completed
    if current_index >= len(question_ids):
        return redirect('quiz:chatbot_results')
    
    # Handle answer submission
    if request.method == 'POST':
        question_id = int(request.POST.get('question_id'))
        answer_id = int(request.POST.get('answer_id'))
        
        # Store answer
        chatbot_data['answers'][str(question_id)] = answer_id
        
        # Check if correct
        is_correct = check_answer(question_id, answer_id)
        if is_correct:
            chatbot_data['score'] = chatbot_data.get('score', 0) + 1
        
        # Move to next question
        chatbot_data['current_question'] = current_index + 1
        request.session['chatbot_data'] = chatbot_data
        
        # Return feedback as JSON for AJAX
        correct_answer = get_correct_answer(question_id)
        return JsonResponse({
            'correct': is_correct,
            'correct_answer': correct_answer.answer_text if correct_answer else None,
            'next': current_index + 1 < len(question_ids)
        })
    
    # Get current question
    question_id = question_ids[current_index]
    question = Question.objects.prefetch_related('answers').get(id=question_id)
    
    # Shuffle answers
    answers = list(question.answers.all())
    random.shuffle(answers)
    
    context = {
        'question': question,
        'answers': answers,
        'question_number': current_index + 1,
        'total_questions': len(question_ids),
        'progress': int((current_index / len(question_ids)) * 100),
        'quiz_title': chatbot_data.get('quiz_title'),
        'step': 4
    }
    return render(request, 'chatbot/quiz.html', context)


def chatbot_results(request):
    """Step 5: Show final results"""
    chatbot_data = request.session.get('chatbot_data', {})
    
    if not chatbot_data.get('questions'):
        return redirect('quiz:chatbot_select_subject')
    
    # Calculate results
    total_questions = len(chatbot_data.get('questions', []))
    score = chatbot_data.get('score', 0)
    percentage = (score / total_questions * 100) if total_questions > 0 else 0
    passed = percentage >= chatbot_data.get('pass_percentage', 70)
    
    # Get quiz object
    quiz = Quiz.objects.get(id=chatbot_data.get('quiz_id'))
    
    # Get or create user
    user, created = User.objects.get_or_create(
        username='chatbot_web_user',
        defaults={'email': 'webuser@chatbot.com'}
    )
    
    # Prepare questions and answers for saving
    questions = Question.objects.filter(id__in=chatbot_data.get('questions', []))
    user_answers = {int(k): v for k, v in chatbot_data.get('answers', {}).items()}
    
    # Save results to database
    try:
        result = save_quiz_result(user, quiz, questions, user_answers)
        result_id = result.id
    except Exception as e:
        result_id = None
        print(f"Error saving results: {e}")
    
    context = {
        'score': score,
        'total': total_questions,
        'percentage': percentage,
        'passed': passed,
        'pass_percentage': chatbot_data.get('pass_percentage'),
        'quiz_title': chatbot_data.get('quiz_title'),
        'subject': chatbot_data.get('subject_name'),
        'difficulty': chatbot_data.get('difficulty'),
        'result_id': result_id,
        'step': 5
    }
    
    # Clear session
    request.session.pop('chatbot_data', None)
    
    return render(request, 'chatbot/results.html', context)


def chatbot_api(request):
    """API endpoint for AJAX requests"""
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'check_answer':
            question_id = data.get('question_id')
            answer_id = data.get('answer_id')
            
            is_correct = check_answer(question_id, answer_id)
            correct_answer = get_correct_answer(question_id)
            
            return JsonResponse({
                'correct': is_correct,
                'correct_answer': correct_answer.answer_text if correct_answer else None
            })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

