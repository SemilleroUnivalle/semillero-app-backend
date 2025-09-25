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

class IsMonitorAcademico(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con tipo 'monitor_academico'
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'monitor_academico'

class IsMonitorAdministrativo(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con tipo 'monitor_administrativo'
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'monitor_administrativo'

class IsProfesorOrAdministrador(permissions.BasePermission):
    """
    Permite acceso a usuarios que son profesores o administradores
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.user_type in ['profesor', 'administrador']
        )

class IsSelfOrAdmin(permissions.BasePermission):
    """
    Solo el propio usuario puede ver/editar su información, excepto los admins
    que pueden ver/editar a cualquiera.
    """
    def has_object_permission(self, request, view, obj):
        # Si es admin, puede ver/editar cualquier objeto
        if request.user.user_type == 'administrador':
            return True
        # Solo puede ver/editar su propio objeto
        return obj.user == request.user  # Cambia a obj == request.user si aplicabr

class IsEstudianteOrProfesor(permissions.BasePermission):
    """
    Permite acceso a usuarios que son estudiantes o profesores
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.user_type in ['estudiante', 'profesor']
        )

class IsEstudianteOrAdministrador(permissions.BasePermission):
    """
    Permite acceso a usuarios que son estudiantes o administradores
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.user_type in ['estudiante', 'administrador']
        )

class IsMonitorAdministrativoOrAdministrador(permissions.BasePermission):
    """
    Permite acceso a usuarios que son monitores administrativos o administradores
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.user_type in ['monitor_administrativo', 'administrador']
        )

class IsMonitorAcademicoOrAdministrador(permissions.BasePermission):
    """
    Permite acceso a usuarios que son monitores académicos o administradores
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.user_type in ['monitor_academico', 'administrador']
        )

class IsProfesorOrAdministradorOrMonitorAcademicoOrAdministrativo(permissions.BasePermission):
    """
    Permite acceso a usuarios que son profesores, administradores, monitores académicos y administrativos
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.user_type in [
                'profesor', 
                'administrador', 
                'monitor_academico', 
                'monitor_administrativo'
            ]
        )

class IsEstudianteOrAdministradorOrMonitorAdministrativo(permissions.BasePermission):
    """
    Permite acceso a usuarios que son estudiantes, administradores o monitores administrativos
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.user_type in [
                'estudiante', 
                'administrador', 
                'monitor_administrativo'
            ]
        )