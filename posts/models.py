from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import Profile

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(max_length=1000)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.author.user.username

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, related_name='commentator', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text