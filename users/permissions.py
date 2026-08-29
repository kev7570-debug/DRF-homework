from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Разрешает доступ только пользователям, состоящим в группе 'moderators'.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='moderators').exists()


class IsOwner(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsNotModerator(permissions.BasePermission):
    """
    Разрешает доступ только пользователям, НЕ состоящим в группе 'moderators'.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.groups.filter(name='moderators').exists()


class IsModeratorOrOwner(permissions.BasePermission):
    """
    Разрешает доступ, если пользователь модератор ИЛИ владелец объекта.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='moderators').exists():
            return True
        return obj.owner == request.user
