from django.db import models
from django.contrib.auth.models import AbstractUser


class Book(models.Model):
    title = models.CharField(max_length=600)
    description = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8,decimal_places=2)

class User(AbstractUser):
     email=models.EmailField(unique=True)
     
     USERNAME_FIELD="email"
     REQUIRED_FIELDS = ['username', 'password']

