# exams/models.py
from django.db import models
from django.contrib.auth.models import User
from worksheets.models import Worksheet, Question

# This model tracks a single attempt by a student on a worksheet.
class ExamAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    worksheet = models.ForeignKey(Worksheet, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True) # e.g., 85.0

    def __str__(self):
        return f"{self.student.username}'s attempt on {self.worksheet.title}"

# This model stores the student's answer for a single question.
class StudentAnswer(models.Model):
    exam_attempt = models.ForeignKey(ExamAttempt, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True, null=True) # For MCQs, this could be 'A', 'B', etc.
    score = models.FloatField(null=True, blank=True, help_text="Score for this specific answer (e.g., out of 5)")
    feedback = models.TextField(blank=True, null=True, help_text="AI-generated feedback for the answer")
    originality_report = models.TextField(blank=True, null=True, help_text="AI-generated report on text originality")


    def __str__(self):
        return f"Answer for Q{self.question.id} in attempt {self.exam_attempt.id}"