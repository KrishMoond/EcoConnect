from django.contrib import admin
from .models import ResourceCategory, Resource, ResourceRating


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'resource_type', 'category', 'is_featured', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['resource_type', 'category', 'is_featured', 'created_at']


@admin.register(ResourceRating)
class ResourceRatingAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
