from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

app_name = 'quiz_api'

# API URL patterns
urlpatterns = [
    # Root API endpoint
    path('', api_views.api_root, name='api_root'),
    
    # Subjects
    path('subjects/', api_views.api_subjects, name='subjects'),
    path('subjects/<str:subject_code>/', api_views.api_subject_detail, name='subject_detail'),
    
    # Questions
    path('questions/', api_views.api_questions, name='questions'),
    
    # Quiz operations
    path('quiz/generate/', api_views.api_generate_quiz, name='generate_quiz'),
    path('quiz/submit/', api_views.api_submit_quiz, name='submit_quiz'),
    
    # Statistics
    path('stats/', api_views.api_quiz_stats, name='stats'),
    
    # Health check
    path('health/', api_views.api_health, name='health'),
]
