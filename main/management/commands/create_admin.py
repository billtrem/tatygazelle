import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Creates a default superuser for Railway deployment using env vars."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")

        # If any required variables are missing, skip safely
        if not username or not password or not email:
            self.stdout.write(self.style.WARNING(
                "Superuser env vars not fully set. "
                "Skipping create_admin. "
                "Expected DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD, DJANGO_SUPERUSER_EMAIL."
            ))
            return

        # Idempotent check by username
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                f"Superuser '{username}' already exists — skipping."
            ))
            return

        # Optional extra safety: prevent duplicate email superusers
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(
                f"A user with email '{email}' already exists. "
                "Skipping to avoid conflicts."
            ))
            return

        self.stdout.write(self.style.WARNING(
            f"Creating superuser '{username}'..."
        ))

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(self.style.SUCCESS(
            f"Superuser '{username}' created successfully."
        ))
