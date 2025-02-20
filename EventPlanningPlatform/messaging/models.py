# messaging/models.py
from django.db import models
from django.conf import settings
from events.models import Event

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='messages')
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message_text[:20]}..."