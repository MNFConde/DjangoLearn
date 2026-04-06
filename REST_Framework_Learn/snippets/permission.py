from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    设置只允许所有者编辑权限
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner
