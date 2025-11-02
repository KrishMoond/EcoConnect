from django.contrib import admin
from .models import Report, ModerationAction


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'reporter', 'report_type', 'status', 'created_at', 'reviewed_by']
    search_fields = ['reason', 'resolution_notes']
    list_filter = ['report_type', 'status', 'created_at']


@admin.register(ModerationAction)
class ModerationActionAdmin(admin.ModelAdmin):
    list_display = ['action_type', 'target_user', 'moderator', 'created_at', 'expires_at']
    search_fields = ['reason']
    list_filter = ['action_type', 'created_at']
