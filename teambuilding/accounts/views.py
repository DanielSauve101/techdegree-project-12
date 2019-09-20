from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserCreateForm


class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('home')
    template_name = "accounts/signup.html"
