from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, FormView

from .forms import UserCreateForm


class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('home')
    template_name = "accounts/signup.html"


class SignInView(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')
    template_name = "accounts/signin.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class SignOutView(RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
