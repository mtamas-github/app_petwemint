# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.urls import reverse
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))

    def getContent(self):

        clean_data = super().clean()
        to_email = clean_data.get('email')

        reset_link = settings.APP_URL + reverse("reset-password")

        msg = f"We have received a request to reset the password for the app.petwemint.com account associated with {to_email}\n"
        msg += f"You can reset your password by clicking the link below: {reset_link} \n\n"
        msg += f"If you did not request to reset your password please let us now by replying this email. \n\n"
        msg += f"PetWeMint team"

        return msg, to_email

    def send(self):

        msg, to_email = self.getContent()
        send_mail('Password reset request', msg, 'admin@petwemint.com', [to_email], fail_silently=False)
        
