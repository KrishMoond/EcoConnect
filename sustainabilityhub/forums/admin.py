from django.contrib import admin
from .models import Category, Topic, Post, TopicLike


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_pinned', 'is_locked', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['category', 'is_pinned', 'is_locked', 'created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['topic', 'author', 'created_at', 'is_edited']
    search_fields = ['content']
    list_filter = ['created_at', 'is_edited']


@admin.register(TopicLike)
class TopicLikeAdmin(admin.ModelAdmin):
    list_display = ['topic', 'user', 'created_at']
