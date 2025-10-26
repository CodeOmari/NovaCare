from django.db import models

import os
import uuid

from django.contrib.auth.models import User




# Adding an Universally Unique Identify(UUID)
# Ensures every uploaded file receive a unique name to avoid collisions
# import uuid and os
def generate_unique_name(instance, filename):
    name = uuid.uuid4() # generates a 32-character hexadecimal string
    full_file_name = f'{name} - {filename}'
    return os.path.join("message_files", full_file_name)


# Create your models here.
# A chat conversation can involve multiple participants
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Display participants in the conversation
        return " | ".join([user.username for user in self.participants.all()])



# Individual messages inside a conversation
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to=generate_unique_name, blank=True, null=True)
    image = models.ImageField(upload_to=generate_unique_name, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('timestamp',)  # latest messages appear last

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'