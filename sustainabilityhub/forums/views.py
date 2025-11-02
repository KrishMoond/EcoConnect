from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Count
from .models import Category, Topic, Post, TopicLike


def home_view(request):
    return render(request, 'index.html')


class CategoryListView(ListView):
    model = Category
    template_name = 'forums/categories.html'
    context_object_name = 'categories'


class TopicListView(ListView):
    model = Topic
    template_name = 'forums/topics.html'
    context_object_name = 'topics'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Topic.objects.annotate(
            post_count=Count('posts')
        ).select_related('author', 'category')
        
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'forums/topic_detail.html'
    context_object_name = 'topic'
    
    def get_object(self):
        topic = get_object_or_404(Topic, pk=self.kwargs['pk'])
        topic.views += 1
        topic.save(update_fields=['views'])
        return topic
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all().select_related('author')
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    template_name = 'forums/topic_form.html'
    fields = ['title', 'content', 'category']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('forums:topic_detail', kwargs={'pk': self.object.pk})


class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    template_name = 'forums/topic_form.html'
    fields = ['title', 'content', 'category']
    
    def get_queryset(self):
        return Topic.objects.filter(author=self.request.user, is_locked=False)
    
    def get_success_url(self):
        return reverse_lazy('forums:topic_detail', kwargs={'pk': self.object.pk})


class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = 'forums/topic_confirm_delete.html'
    success_url = reverse_lazy('forums:topics')
    
    def get_queryset(self):
        return Topic.objects.filter(author=self.request.user)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'forums/post_form.html'
    fields = ['content']
    
    def form_valid(self, form):
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_pk'])
        if topic.is_locked:
            messages.error(self.request, 'This topic is locked.')
            return redirect('forums:topic_detail', pk=topic.pk)
        form.instance.topic = topic
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('forums:topic_detail', kwargs={'pk': self.kwargs['topic_pk']})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'forums/post_form.html'
    fields = ['content']
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def form_valid(self, form):
        form.instance.is_edited = True
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('forums:topic_detail', kwargs={'pk': self.object.topic.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'forums/post_confirm_delete.html'
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('forums:topic_detail', kwargs={'pk': self.object.topic.pk})


def like_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.user.is_authenticated:
        like, created = TopicLike.objects.get_or_create(topic=topic, user=request.user)
        if not created:
            like.delete()
            messages.info(request, 'You unliked this topic.')
        else:
            messages.success(request, 'You liked this topic!')
    return redirect('forums:topic_detail', pk=pk)
