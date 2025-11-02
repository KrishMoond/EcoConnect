from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProjectUpdate
from notifications.utils import create_notification


@receiver(post_save, sender=ProjectUpdate)
def notify_project_update(sender, instance, created, **kwargs):
    """Send notification to project members when a new update is posted"""
    if created:
        project = instance.project
        from django.urls import reverse
        url = reverse('projects:detail', kwargs={'pk': project.pk})
        
        # Notify all project members except the author
        for member in project.members.exclude(id=instance.author.id):
            create_notification(
                recipient=member,
                notification_type='project_update',
                title=f'Update on {project.title}',
                message=instance.content[:100] + '...' if len(instance.content) > 100 else instance.content,
                url=url,
                content_object=instance
            )
        
        # Also notify the creator if they're not a member
        if project.creator not in project.members.all() and project.creator != instance.author:
            create_notification(
                recipient=project.creator,
                notification_type='project_update',
                title=f'Update on {project.title}',
                message=instance.content[:100] + '...' if len(instance.content) > 100 else instance.content,
                url=url,
                content_object=instance
            )

