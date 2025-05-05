from rest_framework import permissions

class IsOwnerOrModeratorOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        is_moderator = request.user.groups.filter(name='Модераторы').exists()

        if request.method == 'POST' and is_moderator:
            return False

        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        is_owner = obj.owner == request.user

        is_moderator = request.user.groups.filter(name='Модераторы').exists()

        if request.method == 'DELETE' and is_moderator:
            return False

        return is_owner or (is_moderator and request.method != 'DELETE')