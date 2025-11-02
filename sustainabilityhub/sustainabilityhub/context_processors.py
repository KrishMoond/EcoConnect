def notifications_count(request):
    """Context processor to add unread notifications count to all templates"""
    if request.user.is_authenticated:
        from notifications.models import Notification
        unread_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}

