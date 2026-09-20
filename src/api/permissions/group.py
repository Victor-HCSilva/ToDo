from rest_framework import permissions


class IsGroupManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.pode_gerenciar(request.user)
