from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from notifications.utils import create_notification


@receiver(post_save, sender=Message)
def notify_new_message(sender, instance, created, **kwargs):
    """Send notification when a new message is received"""
    if created:
        # Get the other participant(s) in the conversation
        conversation = instance.conversation
        recipient = None
        
        for participant in conversation.participants.all():
            if participant != instance.sender:
                recipient = participant
                break
        
        if recipient:
            from django.urls import reverse
            url = reverse('messaging:conversation_detail', kwargs={'pk': conversation.pk})
            
            create_notification(
                recipient=recipient,
                notification_type='message',
                title=f'New message from {instance.sender.username}',
                message=instance.content[:100] + '...' if len(instance.content) > 100 else instance.content,
                url=url,
                content_object=instance
            )

