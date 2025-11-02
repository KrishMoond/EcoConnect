from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from notifications.utils import create_notification


@receiver(post_save, sender=Post)
def notify_topic_reply(sender, instance, created, **kwargs):
    """Send notification when someone replies to a topic"""
    if created and instance.topic.author != instance.author:
        from django.urls import reverse
        url = reverse('forums:topic_detail', kwargs={'pk': instance.topic.pk})
        
        create_notification(
            recipient=instance.topic.author,
            notification_type='topic_reply',
            title=f'New reply to "{instance.topic.title}"',
            message=f'{instance.author.username} replied: {instance.content[:100]}...' if len(instance.content) > 100 else f'{instance.author.username} replied: {instance.content}',
            url=url,
            content_object=instance
        )

