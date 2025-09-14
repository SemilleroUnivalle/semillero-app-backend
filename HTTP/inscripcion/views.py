from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Inscripcion
#Serializadores
from .serializers import InscripcionSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated, AllowAny
#Permisos
from cuenta.permissions import IsAdministrador, IsEstudianteOrAdministrador
#Actions
from rest_framework.decorators import action


class InscripcionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los Inscripciones.
    
    Permite listar, crear, actualizar y eliminar el inscripcion.
    """
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Define permisos para todas las acciones:
        - Los administradores pueden realizar cualquier operación
        - Estudiantes pueden crear inscripciones
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdministrador]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Listar todos los Inscripciones",
        operation_description="Retorna una lista de todos los Inscripciones registrados"
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un inscripcion",
        operation_description="Crea un nuevo registro de inscripcion",
        responses={
            status.HTTP_201_CREATED: InscripcionSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        #Responder con los datos de la nueva inscripción
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener una inscripcion específico",
        operation_description="Retorna los detalles de una inscripcion, específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una inscripcion",        
        operation_description="Actualiza todos los campos de una inscripcion, existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        #Responder con los datos dena inscripcion", actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una inscripcion",
        operation_description="Actualiza uno o más campos de una inscripcion, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una inscripcion",
        operation_description="Elimina permanentemente una inscripcion, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    #Filtros
    @swagger_auto_schema(
        operation_summary="Filtrar inscripcion por tipo de tipo de vinculacion",
        operation_description="Filtra la inscripcion por tipo de vinculacion especificado en los parámetros de la solicitud"
    )
    @action (detail=False, methods=['get'], url_path='filtro-vinculacion',
            permission_classes=[IsAdministrador])
    def filtro_tipo_vinculacion(self, request, *args, **kwargs):
        tipo_vinculacion = request.query_params.get('tipo_vinculacion', None)
        queryset = self.get_queryset()
        if tipo_vinculacion:
            queryset = queryset.filter(tipo_vinculacion=tipo_vinculacion)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Filtrar inscripcion por estado (Activo o Inactivo)",
        operation_description="Filtra la inscripcion por estado especificado en los parámetros de la solicitud"
    )
    @action (detail=False, methods=['get'], url_path='filtro-estado',
            permission_classes=[IsAdministrador])
    def filtro_estado(self, request, *args, **kwargs):
        estado = request.query_params.get('estado', None)
        queryset = self.get_queryset()
        if estado:
            queryset = queryset.filter(estado=estado)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Filtrar inscripcion por grupo",
        operation_description="Filtra la inscripcion por el grupo especificado en los parámetros de la solicitud"
    )
    @action (detail=False, methods=['get'], url_path='filtro-grupo',
            permission_classes=[IsAdministrador])
    def filtro_grupo(self, request, *args, **kwargs):
        grupo = request.query_params.get('grupo', None)
        queryset = self.get_queryset()
        if grupo:
            queryset = queryset.filter(grupo=grupo)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def asignar_grupos():
        pass

