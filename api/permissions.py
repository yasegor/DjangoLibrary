from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_superuser)


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return obj.user == request.user
        return bool(
            request.method in permissions.SAFE_METHODS and obj.user == request.user or
            request.user and
            request.user.is_superuser
        )
        # return bool(request.method in permissions.SAFE_METHODS or obj.user == request.user or request.user.is_superuser)
