from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, null=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    action_dt = models.DateTimeField(default=timezone.now)


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    creation_dt = models.DateTimeField(default=timezone.now)


class Likes(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_dt = models.DateTimeField(default=timezone.now)
