from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ProjectForm, PositionInlineFormSet
from .models import Project, Position


class CreateProjectView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    model = Project

    def get_context_data(self, **kwargs):
        data = super(CreateProjectView, self).get_context_data(**kwargs)
        if self.request.POST:
            data["positions_formset"] = PositionInlineFormSet(self.request.POST)
        else:
            data["positions_formset"] = PositionInlineFormSet()
        return data

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


class UpdateProjectView(LoginRequiredMixin, UpdateView):
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    model = Project

    def get_context_data(self, **kwargs):
        data = super(UpdateProjectView, self).get_context_data(**kwargs)
        if self.request.POST:
            data["positions_formset"] = PositionInlineFormSet(self.request.POST, instance=self.object)
        else:
            data["positions_formset"] = PositionInlineFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        positions = context["positions_formset"]
        self.object = form.save()
        if positions.is_valid():
            positions.instance = self.object
            positions.save()
        return super(UpdateProjectView, self).form_valid(form)


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/project_delete.html"
    success_url = reverse_lazy("home")
