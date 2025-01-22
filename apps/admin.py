from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import User


class UserAdmin(ModelAdmin):
    list_display = (
        'phone', 'name', 'role', 'position', 'phone','is_active')  # 'username' o'rniga 'phone'
    list_filter = ('role', 'is_active')
    search_fields = ('phone', 'name', 'telegram_id')  # 'username'ni 'phone'ga almashtirdik
    ordering = ('-is_active', 'role')

admin.site.register(User, UserAdmin)
