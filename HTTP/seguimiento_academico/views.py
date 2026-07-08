from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import SeguimientoAcademico
#Serializadores
from .serializers import SeguimientoAcademicoSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador


from rest_framework.decorators import action
from profesor.models import Profesor
from inscripcion.models import Inscripcion

class SeguimientoAcademicoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los seguimientos académicos.
    Los profesores solo pueden ver y calificar a los estudiantes de sus grupos asignados.
    """
    queryset = SeguimientoAcademico.objects.all()
    serializer_class = SeguimientoAcademicoSerializer
    permission_classes = [IsAuthenticated, IsProfesorOrAdministrador]

    def get_queryset(self):
        user = self.request.user
        queryset = SeguimientoAcademico.objects.all()

        if user.is_superuser or user.user_type == 'administrador':
            return queryset
        
        if user.user_type == 'profesor':
            # Obtener el profesor asociado al usuario actual
            try:
                profesor = Profesor.objects.get(user=user)
                # Filtrar seguimientos de inscripciones cuyos grupos pertenecen a este profesor
                return queryset.filter(id_inscripcion__grupo__profesor=profesor)
            except Profesor.DoesNotExist:
                return queryset.none()
        
        return queryset.none()

    @swagger_auto_schema(
        operation_summary="Listar estudiantes para seguimiento",
        operation_description="Retorna la lista de inscripciones (estudiantes) de los grupos del profesor con su estado de seguimiento.",
        responses={200: "Lista de estudiantes con sus notas actuales"}
    )
    @action(detail=False, methods=['get'], url_path='estudiantes-seguimiento')
    def estudiantes_seguimiento(self, request):
        """
        Lista todos los estudiantes (inscripciones) que pertenecen a los grupos 
        del profesor autenticado, incluyendo sus notas si ya existen.
        """
        user = request.user
        if user.user_type != 'profesor' and not user.is_superuser:
            return Response({"error": "Solo profesores pueden acceder a esta lista"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            profesor = Profesor.objects.get(user=user)
            # Obtenemos todas las inscripciones del profesor
            inscripciones = Inscripcion.objects.filter(
                grupo__profesor=profesor
            ).select_related('id_estudiante', 'grupo', 'id_modulo')
            
            data = []
            for insc in inscripciones:
                # IMPORTANTE: En Django, acceder a un reverse OneToOneField que no existe
                # lanza RelatedObjectDoesNotExist — getattr(..., None) NO lo captura.
                # Por eso usamos try/except explícito.
                try:
                    seguimiento = insc.seguimiento
                except Exception:
                    seguimiento = None
                
                info = {
                    "id_inscripcion": insc.id_inscripcion,
                    # Campos planos para fácil acceso desde el frontend
                    "nombre": insc.id_estudiante.nombre,
                    "apellido": insc.id_estudiante.apellido,
                    "numero_documento": insc.id_estudiante.numero_documento,
                    "email": insc.id_estudiante.email,
                    "colegio": getattr(insc.id_estudiante, 'colegio', ''),
                    "tipo_vinculacion": insc.tipo_vinculacion,
                    # Campo combinado (retrocompatibilidad)
                    "estudiante_nombre": f"{insc.id_estudiante.nombre} {insc.id_estudiante.apellido}",
                    "documento": insc.id_estudiante.numero_documento,
                    "grupo_nombre": insc.grupo.nombre if insc.grupo else "Sin grupo",
                    "modulo": insc.id_modulo.nombre_modulo if insc.id_modulo else "N/A",
                    "id_seguimiento": seguimiento.id_seguimiento if seguimiento else None,
                    # Notas directamente en el objeto raíz para facilitar mapeo
                    "seguimiento_1": float(seguimiento.seguimiento_1) if seguimiento else None,
                    "seguimiento_2": float(seguimiento.seguimiento_2) if seguimiento else None,
                    "nota_conceptual_docente": float(seguimiento.nota_conceptual_docente) if seguimiento else None,
                    "nota_conceptual_estudiante": float(seguimiento.nota_conceptual_estudiante) if seguimiento else None,
                    "nota_final": float(seguimiento.nota_final) if seguimiento else None,
                    "observaciones": seguimiento.observaciones if seguimiento else "",
                }
                data.append(info)
            
            return Response(data)
        except Profesor.DoesNotExist:
            return Response({"error": "No se encontró perfil de profesor para este usuario"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Crear o actualizar nota",
        operation_description="Crea un seguimiento o actualiza uno existente para una inscripción específica."
    )
    def create(self, request, *args, **kwargs):
        id_inscripcion = request.data.get('id_inscripcion')
        
        if not id_inscripcion:
            return Response({"error": "id_inscripcion es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar que el profesor sea dueño del grupo de esa inscripción
        if request.user.user_type == 'profesor':
            try:
                profesor = Profesor.objects.get(user=request.user)
                if not Inscripcion.objects.filter(id_inscripcion=id_inscripcion, grupo__profesor=profesor).exists():
                    return Response({"error": "No tienes permiso para calificar a este estudiante"}, status=status.HTTP_403_FORBIDDEN)
            except Profesor.DoesNotExist:
                return Response({"error": "No se encontró perfil de profesor"}, status=status.HTTP_404_NOT_FOUND)

        # Si ya existe un seguimiento para esa inscripción, lo actualizamos
        seguimiento = SeguimientoAcademico.objects.filter(id_inscripcion=id_inscripcion).first()
        
        if seguimiento:
            # Al actualizar un OneToOneField, removemos el id_inscripcion de la data 
            # para evitar errores de validación de unicidad, ya que no va a cambiar.
            data = request.data.copy()
            data.pop('id_inscripcion', None)
            serializer = self.get_serializer(seguimiento, data=data, partial=True)
        else:
            serializer = self.get_serializer(data=request.data)
            
        if not serializer.is_valid():
            print(f"DEBUG - Errores de validación: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED if not seguimiento else status.HTTP_200_OK)