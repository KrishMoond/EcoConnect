from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Project, ProjectUpdate


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    paginate_by = 12


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'projects/form.html'
    fields = ['title', 'description', 'status', 'start_date', 'end_date', 'tags', 'image']
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/form.html'
    fields = ['title', 'description', 'status', 'start_date', 'end_date', 'tags', 'image']
    
    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/confirm_delete.html'
    success_url = reverse_lazy('projects:list')
    
    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user)


def join_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user.is_authenticated:
        if request.user not in project.members.all():
            project.members.add(request.user)
            messages.success(request, f'You joined {project.title}!')
        else:
            project.members.remove(request.user)
            messages.info(request, f'You left {project.title}.')
    return redirect('projects:detail', pk=pk)


class ProjectUpdateCreateView(LoginRequiredMixin, CreateView):
    model = ProjectUpdate
    template_name = 'projects/update_form.html'
    fields = ['content']
    
    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form.instance.project = project
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.kwargs['pk']})
