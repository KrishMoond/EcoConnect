from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from .models import ResourceCategory, Resource, ResourceRating


class ResourceCategoryListView(ListView):
    model = ResourceCategory
    template_name = 'resources/categories.html'
    context_object_name = 'categories'


class ResourceListView(ListView):
    model = Resource
    template_name = 'resources/list.html'
    context_object_name = 'resources'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Resource.objects.select_related('author', 'category')
        
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        resource_type = self.request.GET.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ResourceCategory.objects.all()
        return context


class ResourceDetailView(DetailView):
    model = Resource
    template_name = 'resources/detail.html'
    context_object_name = 'resource'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['average_rating'] = self.object.ratings.aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0
        if self.request.user.is_authenticated:
            try:
                context['user_rating'] = self.object.ratings.get(user=self.request.user)
            except ResourceRating.DoesNotExist:
                context['user_rating'] = None
        return context


class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    template_name = 'resources/form.html'
    fields = ['title', 'description', 'resource_type', 'category', 'url', 'image', 'tags', 'is_featured']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('resources:detail', kwargs={'pk': self.object.pk})


class ResourceUpdateView(LoginRequiredMixin, UpdateView):
    model = Resource
    template_name = 'resources/form.html'
    fields = ['title', 'description', 'resource_type', 'category', 'url', 'image', 'tags', 'is_featured']
    
    def get_queryset(self):
        return Resource.objects.filter(author=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('resources:detail', kwargs={'pk': self.object.pk})


class ResourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Resource
    template_name = 'resources/confirm_delete.html'
    success_url = reverse_lazy('resources:list')
    
    def get_queryset(self):
        return Resource.objects.filter(author=self.request.user)


def rate_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.user.is_authenticated and request.method == 'POST':
        rating_value = int(request.POST.get('rating', 0))
        review = request.POST.get('review', '')
        
        if 1 <= rating_value <= 5:
            rating, created = ResourceRating.objects.update_or_create(
                resource=resource,
                user=request.user,
                defaults={'rating': rating_value, 'review': review}
            )
            if created:
                messages.success(request, 'Thank you for rating this resource!')
            else:
                messages.success(request, 'Your rating has been updated.')
        else:
            messages.error(request, 'Invalid rating value.')
    
    return redirect('resources:detail', pk=pk)
