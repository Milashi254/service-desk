from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from services.models import ServiceRequest

DEMO_PASSWORD = 'DemoPass2026!'

# (category, location, description, status)
SAMPLE_REQUESTS = [
    ('streetlight', 'Moi Avenue, Nairobi', 'The streetlight near the bus stop has been out for a week.', 'pending'),
    ('water', 'Kamiti Road, Kahawa', 'No water supply in our block since Monday.', 'in_progress'),
    ('garbage', 'Gikomba Market', 'Rubbish has not been collected for two weeks.', 'resolved'),
    ('road', 'Thika Road, near Roysambu', 'Large pothole that damages passing cars.', 'in_progress'),
    ('streetlight', 'Ngong Road', 'Flickering light near the footbridge.', 'resolved'),
    ('garbage', 'Eastleigh 2nd Avenue', 'Overflowing bins at the market entrance.', 'pending'),
]


class Command(BaseCommand):
    help = 'Create demo users and sample requests for reviewers.'

    def handle(self, *args, **options):
        User = get_user_model()
        citizen, _ = User.objects.get_or_create(
            username='demo_citizen', defaults={'email': 'citizen@example.com'}
        )
        admin, _ = User.objects.get_or_create(
            username='demo_admin', defaults={'email': 'admin@example.com'}
        )
        admin.is_staff = True
        for user in (citizen, admin):
            user.set_password(DEMO_PASSWORD)
            user.save()

        if not ServiceRequest.objects.filter(user=citizen).exists():
            for category, location, description, status in SAMPLE_REQUESTS:
                ServiceRequest.objects.create(
                    user=citizen,
                    category=category,
                    location=location,
                    description=description,
                    status=status,
                )
        self.stdout.write(self.style.SUCCESS('Demo data ready.'))