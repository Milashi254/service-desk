from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    """Sign-up form: username, email and password."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')