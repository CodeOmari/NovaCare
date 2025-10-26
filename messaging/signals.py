from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message

@receiver(post_save, sender=Message)
def notify_message(sender, instance, created, **kwargs):
    if created:
        # Here you could send push, email, or in-app notifications
        print(f"📩 New message from {instance.sender.username} in conversation {instance.conversation.id}")
