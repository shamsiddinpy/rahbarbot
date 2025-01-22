from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField, CharField, Model, TextChoices


class User(AbstractUser):
    class Type(TextChoices):
        SUPER_ADMIN = 'superadmin', 'Superadmin'
        CORP_LEAD = 'corp_lead', 'Corporate Lead'
        ADMIN = 'admin', 'Admin'

    phone = CharField(max_length=20, unique=True)
    name = CharField(max_length=255)
    username = CharField(max_length=255, unique=True)
    role = CharField(max_length=20, choices=Type.choices)
    position = CharField(max_length=255)
    is_active = BooleanField(default=True)  # Todo
    is_staff = BooleanField(default=False)
    telegram_id = CharField(max_length=255, default="0")
    is_superuser = BooleanField(default=False)

    def __str__(self):
        return self.username
