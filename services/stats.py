from django.db.models import Count

from .models import ServiceRequest


def request_stats():
    """Counts shown on the admin dashboard: totals by status and by category."""
    by_status = dict(
        ServiceRequest.objects.order_by().values_list('status').annotate(total=Count('id'))
    )
    by_category = dict(
        ServiceRequest.objects.order_by().values_list('category').annotate(total=Count('id'))
    )
    pending = by_status.get(ServiceRequest.Status.PENDING.value, 0)
    in_progress = by_status.get(ServiceRequest.Status.IN_PROGRESS.value, 0)
    resolved = by_status.get(ServiceRequest.Status.RESOLVED.value, 0)
    total = pending + in_progress + resolved
    return {
        'total': total,
        'open': pending + in_progress,
        'resolved': resolved,
        'resolution_rate': round(resolved * 100 / total) if total else 0,
        'status_chart': {
            'labels': ['Pending', 'In Progress', 'Resolved'],
            'values': [pending, in_progress, resolved],
        },
        'category_chart': {
            'labels': [label for _, label in ServiceRequest.Category.choices],
            'values': [by_category.get(value, 0) for value, _ in ServiceRequest.Category.choices],
        },
    }