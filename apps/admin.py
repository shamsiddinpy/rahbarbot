from django.contrib import admin
from .models import User, Request


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'telegram_id', 'phone', 'role', 'is_active', 'is_staff')
    search_fields = ('name', 'telegram_id', 'phone')
    list_filter = ('is_active', 'role', 'is_staff')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'reason', 'created_at')
    search_fields = ('reason', 'user__name', 'user__telegram_id')
    list_filter = ('created_at', )
