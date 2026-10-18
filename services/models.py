from django.conf import settings
from django.db import models


class ServiceRequest(models.Model):
    """A citizen's request for a public service, such as a broken streetlight."""

    class Category(models.TextChoices):
        STREETLIGHT = 'streetlight', 'Streetlight'
        WATER = 'water', 'Water issue'
        GARBAGE = 'garbage', 'Garbage collection'
        ROAD = 'road', 'Road or pothole'
        OTHER = 'other', 'Other'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests'
    )
    category = models.CharField(max_length=20, choices=Category.choices)
    location = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='requests/', blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_category_display()} at {self.location} ({self.get_status_display()})'