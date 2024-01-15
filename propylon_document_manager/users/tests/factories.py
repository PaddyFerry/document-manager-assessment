from collections.abc import Sequence
from typing import Any

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

from propylon_document_manager.files.models import File


class UserFactory(DjangoModelFactory):
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["email"]


class FileFactory(DjangoModelFactory):
    file_name = Faker("name")
    owner = SubFactory(UserFactory)
    version_number = 1
    created_at = factory.LazyFunction(timezone.now)

    class Meta:
        model = File
