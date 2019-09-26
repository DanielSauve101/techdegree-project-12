from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView

from .forms import ProfileForm, SkillInlineFormSet, UserCreateForm
from .models import Profile


class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("accounts:profile-form")
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
        data = super(CreateProfileView, self).get_context_data(**kwargs)
        if self.request.POST:
            data["skills_formset"] = SkillInlineFormSet(self.request.POST)
        else:
            data["skills_formset"] = SkillInlineFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        skills = context["skills_formset"]
        print(skills)
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
        if skills.is_valid():
            skills.instance = self.object
            skills.save()
        return super(CreateProfileView, self).form_valid(form)


class DetailProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts/profile_detail.html"
