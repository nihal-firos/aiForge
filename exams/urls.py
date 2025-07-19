# exams/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('start/<int:worksheet_pk>/', views.start_exam, name='start_exam'),
    path('attempt/<int:attempt_pk>/', views.take_exam, name='take_exam'),
    path('results/<int:attempt_pk>/', views.exam_results, name='exam_results'), 
]