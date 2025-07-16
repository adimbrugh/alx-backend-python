from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# -----------------------
# 1. Custom User Model
# -----------------------
class User(AbstractUser):
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# -----------------------
# 2. Conversation Model
# -----------------------
class Conversation(models.Model):
    title = models.CharField(max_length=255, blank=True)
    participants = models.ManyToManyField('User', related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} - {self.title or 'Untitled'}"

# -----------------------
# 3. Message Model
# -----------------------
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"
