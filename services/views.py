from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, ServiceRequestForm
from .models import ServiceRequest


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


@login_required
def submit_request(request):
    """Show and process the form for a new service request."""
    form = ServiceRequestForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        service_request = form.save(commit=False)
        service_request.user = request.user
        service_request.save()
        messages.success(request, 'Your request has been submitted.')
        return redirect('request_detail', pk=service_request.pk)
    return render(request, 'services/submit_request.html', {'form': form})


@login_required
def my_requests(request):
    """List the logged-in citizen's own requests, newest first."""
    requests_list = ServiceRequest.objects.filter(user=request.user)
    return render(request, 'services/my_requests.html', {'requests_list': requests_list})


@login_required
def request_detail(request, pk):
    """Show one request. Citizens can only open their own."""
    service_request = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
    return render(request, 'services/request_detail.html', {'service_request': service_request})