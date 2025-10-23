from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
import time

from .models import Subject, Question, get_random_questions, get_all_subjects, get_subject_levels
from .serializers import (
    SubjectSerializer, QuestionSerializer, QuizRequestSerializer,
    QuizSubmissionSerializer, QuizResultSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_subjects(request):
    """
    Get all subjects with their statistics
    
    GET /api/subjects/
    """
    subjects = get_all_subjects()
    serializer = SubjectSerializer(subjects, many=True)
    return Response({
        'success': True,
        'count': subjects.count(),
        'subjects': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_subject_detail(request, subject_code):
    """
    Get specific subject details
    
    GET /api/subjects/{subject_code}/
    """
    try:
        subject = Subject.objects.get(code=subject_code)
        serializer = SubjectSerializer(subject)
        return Response({
            'success': True,
            'subject': serializer.data
        })
    except Subject.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Subject not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_questions(request):
    """
    Get questions with optional filtering
    
    GET /api/questions/?subject_code=CSW351-AI&level=easy&limit=10
    """
    subject_code = request.GET.get('subject_code')
    level = request.GET.get('level')
    limit = int(request.GET.get('limit', 20))
    
    questions = Question.objects.all()
    
    if subject_code:
        questions = questions.filter(subject__code=subject_code)
    
    if level:
        questions = questions.filter(level=level)
    
    questions = questions.order_by('?')[:limit]  # Random order
    
    serializer = QuestionSerializer(questions, many=True)
    return Response({
        'success': True,
        'count': len(questions),
        'questions': serializer.data
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def api_generate_quiz(request):
    """
    Generate a random quiz
    
    POST /api/quiz/generate/
    {
        "subject_code": "CSW351-AI",
        "level": "easy",
        "num_questions": 10
    }
    """
    serializer = QuizRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    subject_code = data['subject_code']
    level = data['level']
    num_questions = data['num_questions']
    
    try:
        # Get random questions
        questions = get_random_questions(subject_code, level, num_questions)
        
        if not questions:
            return Response({
                'success': False,
                'error': f'No questions available for {subject_code} - {level} level'
            }, status=status.HTTP_404_NOT_FOUND)
        
        question_serializer = QuestionSerializer(questions, many=True)
        
        return Response({
            'success': True,
            'quiz': {
                'subject_code': subject_code,
                'level': level,
                'num_questions': len(questions),
                'questions': question_serializer.data
            }
        })
        
    except Subject.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Subject not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_submit_quiz(request):
    """
    Submit quiz answers and get results
    
    POST /api/quiz/submit/
    {
        "answers": [
            {"question_id": 1, "selected_answer": "A"},
            {"question_id": 2, "selected_answer": "B"}
        ]
    }
    """
    serializer = QuizSubmissionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    answers = serializer.validated_data['answers']
    results = []
    correct_count = 0
    
    # Process each answer
    for answer_data in answers:
        question_id = answer_data['question_id']
        selected_answer = answer_data['selected_answer']
        
        try:
            question = Question.objects.get(id=question_id)
            is_correct = selected_answer == question.correct_answer
            
            if is_correct:
                correct_count += 1
            
            results.append({
                'question_id': question_id,
                'question_text': question.question_text,
                'selected_answer': selected_answer,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
                'explanation': question.explanation if question.explanation else None
            })
            
        except Question.DoesNotExist:
            return Response({
                'success': False,
                'error': f'Question with ID {question_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    total_questions = len(results)
    incorrect_count = total_questions - correct_count
    percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    
    result_data = {
        'total_questions': total_questions,
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'percentage': round(percentage, 2),
        'results': results
    }
    
    return Response({
        'success': True,
        'quiz_result': result_data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_quiz_stats(request):
    """
    Get overall quiz statistics
    
    GET /api/stats/
    """
    total_subjects = Subject.objects.count()
    total_questions = Question.objects.count()
    
    # Questions by level
    easy_count = Question.objects.filter(level='easy').count()
    medium_count = Question.objects.filter(level='medium').count()
    hard_count = Question.objects.filter(level='hard').count()
    
    # Questions by subject
    subjects_stats = []
    for subject in Subject.objects.all():
        subjects_stats.append({
            'code': subject.code,
            'name': subject.name,
            'total_questions': subject.total_questions(),
            'easy': subject.questions_by_level('easy').count(),
            'medium': subject.questions_by_level('medium').count(),
            'hard': subject.questions_by_level('hard').count()
        })
    
    return Response({
        'success': True,
        'stats': {
            'total_subjects': total_subjects,
            'total_questions': total_questions,
            'questions_by_level': {
                'easy': easy_count,
                'medium': medium_count,
                'hard': hard_count
            },
            'subjects': subjects_stats
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API root endpoint - shows available endpoints
    
    GET /api/
    """
    return Response({
        'success': True,
        'message': 'Welcome to Quiz System API',
        'version': '1.0.0',
        'endpoints': {
            'subjects': '/api/subjects/',
            'subject_detail': '/api/subjects/{code}/',
            'questions': '/api/questions/',
            'generate_quiz': '/api/quiz/generate/',
            'submit_quiz': '/api/quiz/submit/',
            'stats': '/api/stats/',
            'health': '/api/health/'
        },
        'documentation': 'See API_DOCUMENTATION.md for detailed usage',
        'browsable_api': 'Visit /api/ in browser for interactive API browser'
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_health(request):
    """
    Health check endpoint
    
    GET /api/health/
    """
    return Response({
        'success': True,
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0'
    })
