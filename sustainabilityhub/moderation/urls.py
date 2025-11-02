from django.urls import path
from .views import (
    ReportListView, ReportCreateView, ReportDetailView,
    ReportUpdateView, ModerationActionListView
)

app_name = 'moderation'

urlpatterns = [
    path('reports/', ReportListView.as_view(), name='reports'),
    path('reports/create/', ReportCreateView.as_view(), name='report_create'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('reports/<int:pk>/update/', ReportUpdateView.as_view(), name='report_update'),
    path('actions/', ModerationActionListView.as_view(), name='actions'),
]

