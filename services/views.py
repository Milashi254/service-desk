from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegisterForm


@login_required
def home(request):
    """Landing page shown after login."""
    return render(request, 'home.html')


def register(request):
    """Let a new citizen create an account, then log them in."""
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Welcome! Your account has been created.')
        return redirect('home')
    return render(request, 'registration/register.html', {'form': form})