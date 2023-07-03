from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperuser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or request.user.is_staff))


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


__all__ = [
    'IsSuperuser',
    'IsStaff',
    'IsAdmin',
    'IsAuthenticated',
    'ReadOnly',
]
