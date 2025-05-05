from rest_framework import permissions

class IsOwnerOrModeratorOrReadOnly(permissions.BasePermission): 
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        is_moderator = request.user.groups.filter(name='Модераторы').exists()
        
        if request.method == 'POST' and is_moderator:
            return False

        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'user'):
            is_owner = obj.user == request.user
        elif hasattr(obj, 'owner'):
            is_owner = obj.owner == request.user
        else:
            is_owner = False

        is_moderator = request.user.groups.filter(name='Модераторы').exists()

        if request.method == 'DELETE' and is_moderator:
            return False

        return is_owner or (is_moderator and request.method != 'DELETE')

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
            
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
            
        return obj == request.user or request.user.is_staff