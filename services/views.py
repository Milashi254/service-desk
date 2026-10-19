from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import citizen_required, staff_required
from .forms import RegisterForm, ServiceRequestForm, StatusForm
from .models import ServiceRequest
from .stats import request_stats


def home(request):
    """Public landing page. Staff are sent straight to the dashboard."""
    if request.user.is_staff:
        return redirect('admin_dashboard')
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


@citizen_required
def submit_request(request):
    """Show and process the form for a new service request."""
    form = ServiceRequestForm(
        request.POST or None,
        request.FILES or None,
        initial={'category': request.GET.get('category', '')},
    )
    if form.is_valid():
        service_request = form.save(commit=False)
        service_request.user = request.user
        service_request.save()
        messages.success(request, 'Your request has been submitted.')
        return redirect('request_detail', pk=service_request.pk)
    return render(request, 'services/submit_request.html', {'form': form})


@citizen_required
def my_requests(request):
    """List the logged-in citizen's own requests, newest first."""
    requests_list = ServiceRequest.objects.filter(user=request.user)
    return render(request, 'services/my_requests.html', {'requests_list': requests_list})


@citizen_required
def request_detail(request, pk):
    """Show one request. Citizens can only open their own."""
    service_request = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
    return render(request, 'services/request_detail.html', {'service_request': service_request})


@staff_required
def admin_dashboard(request):
    """Staff-only list of all requests, with status and category filters."""
    requests_list = ServiceRequest.objects.select_related('user')
    status = request.GET.get('status', '')
    category = request.GET.get('category', '')
    if status in ServiceRequest.Status.values:
        requests_list = requests_list.filter(status=status)
    if category in ServiceRequest.Category.values:
        requests_list = requests_list.filter(category=category)
    context = {
        'requests_list': requests_list,
        'statuses': ServiceRequest.Status.choices,
        'categories': ServiceRequest.Category.choices,
        'selected_status': status,
        'selected_category': category,
        'stats': request_stats(),
    }
    return render(request, 'services/admin_dashboard.html', context)


@staff_required
def admin_request_detail(request, pk):
    """Staff view of any request, with a form to change its status."""
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    form = StatusForm(request.POST or None, instance=service_request)
    if form.is_valid():
        form.save()
        messages.success(request, 'Status updated.')
        return redirect('admin_request_detail', pk=pk)
    return render(
        request,
        'services/admin_request_detail.html',
        {'service_request': service_request, 'form': form},
    )