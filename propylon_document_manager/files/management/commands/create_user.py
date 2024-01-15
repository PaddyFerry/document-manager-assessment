from django.core.management.base import BaseCommand

from propylon_document_manager.users.models import User


class Command(BaseCommand):
    help = 'Create user'

    def handle(self, *args, **kwargs):
        User.objects.get_or_create(
            name="username",
            email="test@email.com",
            password="123456",
            is_active=True,
        )
