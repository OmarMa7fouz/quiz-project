from django.urls import path
from . import views, chatbot_views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('results/<int:result_id>/', views.view_results, name='view_results'),
    
    # Chatbot routes (simplified - only for subject/difficulty selection)
    path('chatbot/', chatbot_views.chatbot_home, name='chatbot_home'),
    path('chatbot/subject/', chatbot_views.chatbot_select_subject, name='chatbot_select_subject'),
    path('chatbot/difficulty/', chatbot_views.chatbot_select_difficulty, name='chatbot_select_difficulty'),
]

