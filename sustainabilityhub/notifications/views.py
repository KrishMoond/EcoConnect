from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    
    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_count'] = Notification.objects.filter(
            recipient=self.request.user,
            is_read=False
        ).count()
        return context


def mark_as_read(request, pk):
    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user
    )
    notification.is_read = True
    notification.save()
    
    if notification.url:
        return redirect(notification.url)
    return redirect('notifications:list')


def mark_all_as_read(request):
    if request.user.is_authenticated:
        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
    return redirect('notifications:list')


def delete_notification(request, pk):
    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user
    )
    notification.delete()
    messages.success(request, 'Notification deleted.')
    return redirect('notifications:list')
