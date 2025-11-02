from django.db import models
from django.conf import settings
from django.utils import timezone


class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('workshop', 'Workshop'),
        ('conference', 'Conference'),
        ('meetup', 'Meetup'),
        ('webinar', 'Webinar'),
        ('volunteer', 'Volunteer Activity'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='meetup')
    location = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    max_participants = models.IntegerField(null=True, blank=True)
    image = models.FileField(upload_to='events/', null=True, blank=True)
    is_online = models.BooleanField(default=False)
    online_link = models.URLField(blank=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attending_events', blank=True)
    
    class Meta:
        ordering = ['start_date']
    
    def __str__(self):
        return self.title
    
    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()
    
    @property
    def participant_count(self):
        return self.participants.count()
