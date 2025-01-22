from rest_framework.permissions import BasePermission

from apps.models import User


class IsSuperAdmin(BasePermission):
    """
    Faqat superadmin foydalanuvchilariga ruxsat berish.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == User.Type.SUPER_ADMIN
        )
