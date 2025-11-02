from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Report, ModerationAction


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'moderation/reports.html'
    context_object_name = 'reports'
    
    def get_queryset(self):
        queryset = Report.objects.select_related('reporter', 'reviewed_by')
        # Regular users can only see their own reports
        if not self.request.user.is_staff:
            queryset = queryset.filter(reporter=self.request.user)
        return queryset.order_by('-created_at')


class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    template_name = 'moderation/report_form.html'
    fields = ['report_type', 'reason']
    
    def form_valid(self, form):
        form.instance.reporter = self.request.user
        
        # Get content type and object ID from POST data
        content_type_id = self.request.POST.get('content_type_id')
        object_id = self.request.POST.get('object_id')
        
        if content_type_id and object_id:
            form.instance.content_type_id = content_type_id
            form.instance.object_id = object_id
        
        messages.success(self.request, 'Report submitted successfully. Thank you for helping keep our community safe.')
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect back to the reported content or home
        return self.request.POST.get('next', reverse_lazy('forums:topics'))


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'moderation/report_detail.html'
    context_object_name = 'report'
    
    def get_queryset(self):
        queryset = Report.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(reporter=self.request.user)
        return queryset


class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    template_name = 'moderation/report_form.html'
    fields = ['status', 'resolution_notes']
    
    def get_queryset(self):
        # Only staff can update reports
        if self.request.user.is_staff:
            return Report.objects.all()
        return Report.objects.none()
    
    def form_valid(self, form):
        if not form.instance.reviewed_by:
            form.instance.reviewed_by = self.request.user
            form.instance.reviewed_at = timezone.now()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('moderation:report_detail', kwargs={'pk': self.object.pk})


class ModerationActionListView(LoginRequiredMixin, ListView):
    model = ModerationAction
    template_name = 'moderation/actions.html'
    context_object_name = 'actions'
    
    def get_queryset(self):
        # Only staff can view moderation actions
        if self.request.user.is_staff:
            return ModerationAction.objects.select_related(
                'moderator', 'target_user'
            ).order_by('-created_at')
        return ModerationAction.objects.none()
