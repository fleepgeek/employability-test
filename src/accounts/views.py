from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.conf import settings

from .forms import ApplicantRegisterForm

User = settings.AUTH_USER_MODEL

class RegisterView(CreateView):
    # model = User
    form_class = ApplicantRegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login'

