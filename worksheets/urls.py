# worksheets/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_worksheet, name='create_worksheet'),
    path('<int:pk>/', views.worksheet_detail, name='worksheet_detail'),
    path('<int:pk>/download/', views.download_worksheet_pdf, name='download_worksheet_pdf'), 
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('<int:worksheet_pk>/attempts/', views.worksheet_attempts, name='worksheet_attempts'),
]