from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Grupo
#Serializadores
from .serializers import GrupoSerializer
from grupo.serializers import GrupoListaSerializer 
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador
#action
from rest_framework.decorators import action

class GrupoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los grupos.
    
    Permite listar, crear, actualizar y eliminar el grupo.
    """
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Define permisos para todas las acciones:
        - Solo los administradores pueden realizar cualquier operación
        - Estudiantes y profesores no tienen acceso
        """
        permission_classes = [IsAuthenticated, IsAdministrador]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Listar todos los grupos",
        operation_description="Retorna una lista de todos los grupos registrados"
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un grupo",
        operation_description="Crea un nuevo registro de grupo",
        responses={
            status.HTTP_201_CREATED: GrupoSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        #Responder con los datos del nuevna grupo",
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener una grupo específico",
        operation_description="Retorna los detalles de una grupo, específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una grupo",        
        operation_description="Actualiza todos los campos de una grupo, existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        #Responder con los datos dena grupo", actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una grupo",
        operation_description="Actualiza uno o más campos de una grupo, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una grupo",
        operation_description="Elimina permanentemente una grupo, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    #Grupos por profesor
    @action(detail=False, methods=['get'], url_path="grupo-profesor",
            permission_classes=[IsAdministrador])
    def grupo_profesor(self, request):
        """
        Obtiene los detalles de un grupo específico incluyendo estudiantes.
        Parámetros: grupo_id (requerido)
        """
        grupo_id = request.query_params.get('grupo', None)
        
        if not grupo_id:
            return Response({'detail': 'El parámetro grupo_id es requerido.'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Obtener el grupo específico con optimización de consultas
            grupo = Grupo.objects.select_related('monitor_academico').prefetch_related(
                'matricula__id_estudiante'
            ).get(id=grupo_id)
            
        except Grupo.DoesNotExist:
            return Response({'detail': 'Grupo no encontrado.'}, 
                           status=status.HTTP_404_NOT_FOUND)
        
        # Usar GrupoListaSerializer para un solo objeto (sin many=True)
        serializer = GrupoListaSerializer(grupo, context={'request': request})
        return Response(serializer.data)