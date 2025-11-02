from django.urls import path
from .views import (
    ResourceCategoryListView, ResourceListView, ResourceDetailView,
    ResourceCreateView, ResourceUpdateView, ResourceDeleteView,
    rate_resource
)

app_name = 'resources'

urlpatterns = [
    path('', ResourceListView.as_view(), name='list'),
    path('categories/', ResourceCategoryListView.as_view(), name='categories'),
    path('<int:pk>/', ResourceDetailView.as_view(), name='detail'),
    path('create/', ResourceCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', ResourceUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ResourceDeleteView.as_view(), name='delete'),
    path('<int:pk>/rate/', rate_resource, name='rate'),
]

