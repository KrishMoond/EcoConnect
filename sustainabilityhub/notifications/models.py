from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('message', 'New Message'),
        ('project_update', 'Project Update'),
        ('event_reminder', 'Event Reminder'),
        ('topic_reply', 'Topic Reply'),
        ('mention', 'Mention'),
        ('like', 'Like'),
        ('follow', 'Follow'),
        ('other', 'Other'),
    ]
    
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True)
    
    # Generic foreign key for linking to various content types
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.notification_type} notification for {self.recipient.username}'
