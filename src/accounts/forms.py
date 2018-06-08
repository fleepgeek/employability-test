from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import transaction

from .models import Applicant

# User = settings.AUTH_USER_MODEL
User = get_user_model()

class ApplicantRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password2(self):
        data = self.cleaned_data
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords you entered are not the same')
        return password1

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        applicant = Applicant.objects.create(user=user)
        return user