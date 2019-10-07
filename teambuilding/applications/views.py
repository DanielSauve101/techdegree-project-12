from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from projects.models import Project
from .models import Applicant


class ListApplicationsView(LoginRequiredMixin, ListView):
    model = Applicant
    template_name = "applications/applications.html"


class CreateApplicantView(CreateView):
    model = Applicant
    template_name = "applications/applicant_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(slug=self.kwargs.get('slug'))
        return super(CreateApplicantView, self).form_valid(form)

