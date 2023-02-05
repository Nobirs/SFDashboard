from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Token


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="User Email")

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password1',
            'password2',
        )


class SignUpTokenForm(forms.ModelForm):
    token = forms.CharField(max_length=100)

    class Meta:
        model = Token
        fields = (
            'token',
        )



