from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


TYPE_CHOICES= [
    ('Student', 'Student'),
    ('Educator', 'Educator'),
    ]

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=8, choices=TYPE_CHOICES, default='Student')


#class CustomUser(AbstractUser):
 #   user_type = models.PositiveIntegerField(null=True, blank=True)
