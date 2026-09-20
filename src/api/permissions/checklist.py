from rest_framework import permissions


class IsChecklistOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user", None) == request.user
