from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """
    Требование прав администратора на все операции.
    """
    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return request.user.is_admin

        return False


class IsAdminOrReadOnly(BasePermission):
    """
    Требование прав администратора для операций записи.
    """
    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.is_admin

        return False
