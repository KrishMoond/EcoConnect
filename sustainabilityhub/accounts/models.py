from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return self.username