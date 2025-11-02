from django.contrib import admin
from .models import Project, ProjectUpdate


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'status', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['status', 'created_at']
    filter_horizontal = ['members']


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ['project', 'author', 'created_at']
    search_fields = ['content']
    list_filter = ['created_at']
