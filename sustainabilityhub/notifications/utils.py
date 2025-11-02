from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .models import Notification


def create_notification(recipient, notification_type, title, message, url='', content_object=None):
    """Helper function to create notifications"""
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        url=url,
    )
    
    if content_object:
        notification.content_type = ContentType.objects.get_for_model(content_object)
        notification.object_id = content_object.pk
        notification.save()
    
    return notification

