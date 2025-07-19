# worksheets/models.py
from django.db import models
# from django.contrib.auth.models import User # For later

class Worksheet(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=50, help_text="e.g., '6th Grade'")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('short_answer', 'Short Answer'),
    ]
    worksheet = models.ForeignKey(Worksheet, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    options = models.JSONField(null=True, blank=True, help_text="For MCQs, e.g., {'A': 'Option 1'}")
    correct_answer = models.TextField(help_text="For MCQs, just the letter 'A'. For short answers, the model answer.")

    def __str__(self):
        return self.text[:50] + "..."

