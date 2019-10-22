from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView

from .forms import (MyProjectInlineFormSet, ProfileForm, 
                    SkillInlineFormSet, UserCreateForm)
from .models import Profile


class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("accounts:profile-create")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid


class LogInView(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/login.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogOutView(RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class CreateProfileView(LoginRequiredMixin, CreateView):
    form_class = ProfileForm
    template_name = "accounts/profile_form.html"
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(CreateProfileView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["skills_formset"] = SkillInlineFormSet(self.request.POST)
            context["my_project_formset"] = MyProjectInlineFormSet(
                self.request.POST
                )
        else:
            context["skills_formset"] = SkillInlineFormSet()
            context["my_project_formset"] = MyProjectInlineFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        skills = context["skills_formset"]
        my_projects = context["my_project_formset"]
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
        if skills.is_valid() and my_projects.is_valid():
            skills.instance = self.object
            skills.save()
            my_projects.instance = self.object
            my_projects.save()
        return super(CreateProfileView, self).form_valid(form)


class DetailProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts/profile_detail.html"


class UpdateProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ProfileForm
    template_name = "accounts/profile_form.html"
    model = Profile

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super(UpdateProfileView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["skills_formset"] = SkillInlineFormSet(
                self.request.POST, instance=self.object
                )
            context["my_project_formset"] = MyProjectInlineFormSet(
                self.request.POST, instance=self.object
                )
        else:
            context["skills_formset"] = SkillInlineFormSet(
                instance=self.object
                )
            context["my_project_formset"] = MyProjectInlineFormSet(
                instance=self.object
                )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        skills = context["skills_formset"]
        my_projects = context["my_project_formset"]
        self.object = form.save()
        if skills.is_valid() and my_projects.is_valid():
            skills.instance = self.object
            skills.save()
            my_projects.instance = self.object
            my_projects.save()
        return super(UpdateProfileView, self).form_valid(form)
