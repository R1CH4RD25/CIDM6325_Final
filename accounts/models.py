from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


FRUIT_CHOICES= [
    ('orange', 'Oranges'),
    ('cantaloupe', 'Cantaloupes'),
    ('mango', 'Mangoes'),
    ('honeydew', 'Honeydews'),
    ]




class CustomUser(AbstractUser):
    user_type = models.PositiveIntegerField(null=True, blank=True)
