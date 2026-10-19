from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from services.models import ServiceRequest

CITIZEN_USERNAME, CITIZEN_PASSWORD = 'Milka', 'Milka2026'
ADMIN_USERNAME, ADMIN_PASSWORD = 'admin', 'admin2026'

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

        # Older versions used 'demo_citizen' and 'demo_admin'. Rename the citizen
        # (keeping its requests) and remove the old demo admin.
        if not User.objects.filter(username=CITIZEN_USERNAME).exists():
            User.objects.filter(username='demo_citizen').update(username=CITIZEN_USERNAME)
        User.objects.filter(username='demo_admin').delete()

        citizen, _ = User.objects.get_or_create(
            username=CITIZEN_USERNAME, defaults={'email': 'citizen@example.com'}
        )
        admin, _ = User.objects.get_or_create(
            username=ADMIN_USERNAME, defaults={'email': 'admin@example.com'}
        )

        citizen.is_staff = False
        admin.is_staff = True
        admin.is_superuser = False  # the public demo admin can only use the dashboard
        for user, password in ((citizen, CITIZEN_PASSWORD), (admin, ADMIN_PASSWORD)):
            user.set_password(password)
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