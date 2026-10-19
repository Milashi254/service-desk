from django.contrib import admin

from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    """Show service requests in Django's built-in admin area."""

    list_display = ('id', 'category', 'location', 'user', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('location', 'description', 'user__username')