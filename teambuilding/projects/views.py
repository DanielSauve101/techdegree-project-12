from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import ProjectForm, PositionInlineFormSet
from .models import Applicant, Project, Position


class CreateProjectView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["positions_formset"] = PositionInlineFormSet(self.request.POST)
        else:
            context["positions_formset"] = PositionInlineFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        positions = context["positions_formset"]
        with transaction.atomic():
            form.instance.project_owner = self.request.user
            self.object = form.save()
        if positions.is_valid():
            positions.instance = self.object
            positions.save()
        return super(CreateProjectView, self).form_valid(form)


class DetailProjectView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"


class UpdateProjectView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    model = Project

    def test_func(self):
        obj = self.get_object()
        return obj.project_owner == self.request.user

    def get_context_data(self, **kwargs):
        context = super(UpdateProjectView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["positions_formset"] = PositionInlineFormSet(self.request.POST, instance=self.object)
        else:
            context["positions_formset"] = PositionInlineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        positions = context["positions_formset"]
        self.object = form.save()
        if positions.is_valid():
            positions.instance = self.object
            positions.save()
        return super(UpdateProjectView, self).form_valid(form)


class DeleteProjectView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = "projects/project_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        obj = self.get_object()
        return obj.project_owner == self.request.user


class ListApplicationsView(LoginRequiredMixin, ListView):
    model = Applicant
    template_name = "projects/applications.html"

    def get_queryset(self):
        filter_value = self.request.GET.get('filter', 'All Applications')
        if filter_value == 'All Applications':
            queryset = Applicant.objects.all()
        else:
            queryset = Applicant.objects.filter(
                status__icontains=filter_value[0:3]
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListApplicationsView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter')
        return context



class CreateApplicantView(LoginRequiredMixin, CreateView):
    model = Applicant
    template_name = "projects/applicant_form.html"
    success_url = reverse_lazy("home")
    fields = ['status']

    def get_context_data(self, **kwargs):
        context = super(CreateApplicantView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(slug=self.kwargs.get('slug'))
        context['position'] = Position.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.user = self.request.user
        form.instance.project = context['project']
        form.instance.position = context['position']
        return super(CreateApplicantView, self).form_valid(form)


class UpdateApplicantView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Applicant
    template_name = "projects/applicant_edit_form.html"
    success_url = reverse_lazy("projects:applications-list")
    fields = ['status']

    def test_func(self):
        obj = self.get_object()
        return obj.project.project_owner == self.request.user

    def form_valid(self, form):
        position = self.object.position
        status = form.cleaned_data.get('status')

        if status == 'ACC':
            status = 'Congradulations! You have been accepted for the {} position.'.format(position)
        else:
            status = 'We regret to inform you that you have been rejected for the {} position.'.format(position)

        send_mail(
            self.object.project,
            status,
            self.request.user.email,
            [self.object.user.email],
            fail_silently=False,
            )
        return super(UpdateApplicantView, self).form_valid(form)