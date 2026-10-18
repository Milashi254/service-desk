from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('requests/new/', views.submit_request, name='submit_request'),
    path('requests/', views.my_requests, name='my_requests'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/<int:pk>/', views.admin_request_detail, name='admin_request_detail'),
]