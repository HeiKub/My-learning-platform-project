# topics/urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('', views.topic_list, name ='topic-list'),
    path('<int:topic_id>', views.topic_detail, name ='topic-detail'),
    path('topics/<int:topic_id>/quizzes/', views.quizzes_for_topic, name='quizzes_for_topic'),
    path('quizzes/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quizzes/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),


]

