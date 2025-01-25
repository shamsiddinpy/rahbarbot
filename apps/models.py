from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField, CharField, Model, TextChoices, TextField, ForeignKey, CASCADE, FileField, \
    DateTimeField


class User(AbstractUser):
    class Type(TextChoices):
        SUPER_ADMIN = 'superadmin', 'Superadmin'
        CORP_LEAD = 'corp_lead', 'Corporate Lead'
        ADMIN = 'admin', 'Admin'

    phone = CharField(max_length=20, unique=True, blank=True, null=True)
    name = CharField(max_length=255)
    username = CharField(max_length=255, blank=True, null=True, unique=True)
    role = CharField(max_length=20, choices=Type.choices)
    position = CharField(max_length=255)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    telegram_id = CharField(max_length=255, default="0", unique=True)
    is_superuser = BooleanField(default=False)
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100, blank=True, null=True)
    expense = TextField(blank=True)

    def __str__(self):
        return self.username


class Request(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='requests')
    reason = TextField('Murojaat sababi', null=True, blank=True)
    attachment = FileField('Foto/Video fayl', upload_to='attachments/', null=True, blank=True)
    full_name = TextField("Foydalanuvchi haqida ma'lumot", null=True, blank=True)
    phone_number = CharField(max_length=20, null=True, blank=True)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            username = self.user.username if self.user and self.user.username else "Unknown User"
            created_at = self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else "Unknown Date"
            return f"Request by {username} at {created_at}"
        except Exception as e:
            return "Invalid Request"
