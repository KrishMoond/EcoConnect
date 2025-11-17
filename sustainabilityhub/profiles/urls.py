from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('edit/', views.profile_edit, name='edit'),
    path('bookmarks/', views.my_bookmarks, name='bookmarks'),
    path('feed/', views.activity_feed, name='feed'),
    path('bookmark/toggle/', views.toggle_bookmark, name='toggle_bookmark'),
    path('follow/<str:username>/', views.follow_user, name='follow'),
    path('<str:username>/', views.profile_detail, name='detail'),
]
