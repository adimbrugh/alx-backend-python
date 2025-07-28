from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models import Prefetch
from messaging.models import Message



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_messages')

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} | Message: {self.message.id}"



class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Edit by {self.edited_by} on {self.edited_at}"



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content[:30]}"



def get_conversation_with_threads(user1, user2):
    base_messages = Message.objects.filter(
        sender__in=[user1, user2],
        receiver__in=[user1, user2],
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).order_by('timestamp')

    return base_messages



def fetch_thread(message):
    """ Recursively fetch all nested replies to a message """
    thread = []
    replies = message.replies.all().select_related('sender', 'receiver')
    for reply in replies:
        thread.append({
            'message': reply,
            'replies': fetch_thread(reply)  # recurse
        })
    return thread
