# users/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES)

    def __str__(self):
        return f'{self.user.username} - {self.role}'