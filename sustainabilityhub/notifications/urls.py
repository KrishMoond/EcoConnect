from django.urls import path
from .views import (
    NotificationListView, mark_as_read, mark_all_as_read,
    delete_notification
)

app_name = 'notifications'

urlpatterns = [
    path('', NotificationListView.as_view(), name='list'),
    path('<int:pk>/read/', mark_as_read, name='mark_read'),
    path('mark-all-read/', mark_all_as_read, name='mark_all_read'),
    path('<int:pk>/delete/', delete_notification, name='delete'),
]

