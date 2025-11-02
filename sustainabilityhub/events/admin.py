from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'event_type', 'start_date', 'location']
    search_fields = ['title', 'description']
    list_filter = ['event_type', 'start_date', 'is_online']
    filter_horizontal = ['participants']
