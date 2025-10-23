from django.urls import path
from . import views, chatbot_views

app_name = 'quiz'

urlpatterns = [
    # Home - Select subject
    path('', views.home, name='home'),
    
    # Quiz list - Show all subjects
    path('quizzes/', views.quiz_list, name='quiz_list'),
    
    # Select difficulty for a subject
    path('subject/<str:subject_code>/', views.select_difficulty, name='select_difficulty'),
    
    # Take quiz
    path('quiz/<str:subject_code>/<str:level>/', views.take_quiz, name='take_quiz'),
    
    # Check answers (AJAX)
    path('check-answers/', views.check_answers, name='check_answers'),
    
    # Chatbot routes
    path('chatbot/', chatbot_views.chatbot_home, name='chatbot_home'),
    path('chatbot/select-subject/', chatbot_views.chatbot_select_subject, name='chatbot_select_subject'),
    path('chatbot/select-difficulty/', chatbot_views.chatbot_select_difficulty, name='chatbot_select_difficulty'),
    path('chatbot/start-quiz/', chatbot_views.chatbot_start_quiz, name='chatbot_start_quiz'),
]
