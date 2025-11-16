from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser

from shop.models import CustomUser
from .models import Comment


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "password"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "re-password"
    }))

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "your email"
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "your name"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "your last_name"
            })
        }


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "your email",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "your password",
    }))

    class Meta:
        model = CustomUser
        fields = ["email", 'password']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Izoh yozing...'})
        }