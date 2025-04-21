from rest_framework import permissions

class IsEstudiante(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con tipo 'estudiante'
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'estudiante'

class IsProfesor(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con tipo 'profesor'
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'profesor'

class IsAdministrador(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con tipo 'administrador'
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'administrador'

class IsProfesorOrAdministrador(permissions.BasePermission):
    """
    Permite acceso a usuarios que son profesores o administradores
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.user_type in ['profesor', 'administrador']