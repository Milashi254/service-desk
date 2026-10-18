from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ServiceRequest


class RegisterForm(UserCreationForm):
    """Sign-up form: username, email and password."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')


class ServiceRequestForm(forms.ModelForm):
    """Form a citizen fills in to report a problem."""

    class Meta:
        model = ServiceRequest
        fields = ('category', 'location', 'description', 'image')
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}
        

class StatusForm(forms.ModelForm):
    """Lets staff change the status of a request."""

    class Meta:
        model = ServiceRequest
        fields = ('status',)