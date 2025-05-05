from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from collections import defaultdict

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Modulo
#Serializadores
from .serializers import ModuloReadSerializer, ModuloWriteSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador


class ModuloViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los Modulos.
    
    Permite listar, crear, actualizar y eliminar Modulos.
    """
    queryset = Modulo.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Usa el serializador correcto según el método:
        - Para GET (list, retrieve): ModuloReadSerializer con depth=1
        - Para POST, PUT, PATCH: ModuloWriteSerializer sin depth
        """
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ModuloWriteSerializer
        return ModuloReadSerializer

    def get_permissions(self):
        """
        Define permisos para todas las acciones:
        - Solo los administradores pueden realizar cualquier operación
        - Estudiantes y profesores no tienen acceso
        """
        permission_classes = [IsAuthenticated, IsAdministrador]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Listar todos los modulos",
        operation_description="Retorna todos los modulos registrados por el administrador"
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response({"No hay modulos registrados"}, status=status.HTTP_204_NOT_CONTENT)
        
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un modulo",
        operation_description="Crea un nuevo modulo en el sistema",
        request_body=ModuloWriteSerializer,
        responses={
            status.HTTP_201_CREATED: ModuloReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            # Obtener el objeto creado y devolverlo con el serializador de lectura
            instance = serializer.instance
            read_serializer = ModuloReadSerializer(instance)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detalle": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Obtener un modulo específico",
        operation_description="Retorna los detalles de un modulo específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar un modulo",        
        operation_description="Actualiza todos los campos de un modulo existente",
        request_body=ModuloWriteSerializer,
        responses={
            status.HTTP_200_OK: ModuloReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_update(serializer)
            # Devolver respuesta con el serializador de lectura para mostrar relaciones
            read_serializer = ModuloReadSerializer(instance)
            return Response(read_serializer.data)
        except ValidationError as e:
            return Response({"detalle": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente un modulo",
        operation_description="Actualiza uno o más campos de un modulo existente",
        request_body=ModuloWriteSerializer,
        responses={
            status.HTTP_200_OK: ModuloReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar un Modulo",
        operation_description="Elimina permanentemente un Modulo del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Listar módulos por categoría",
        operation_description="Retorna los módulos agrupados por categoría",
        manual_parameters=[
            openapi.Parameter(
                'solo_activos', 
                openapi.IN_QUERY, 
                description="Filtrar solo módulos activos (true/false)", 
                type=openapi.TYPE_BOOLEAN,
                default=True
            )
        ],
        responses={
            status.HTTP_200_OK: "Módulos agrupados por categoría",
            status.HTTP_204_NO_CONTENT: "No hay módulos registrados"
        }
    )
    @action(detail=False, methods=['get'], url_path='por-categoria')
    def listar_por_categoria(self, request):
        """
        Endpoint para listar los módulos agrupados por categoría.
        """
        solo_activos = request.query_params.get('solo_activos', 'true').lower() == 'true'
        
        # Obtener todos los módulos con sus categorías en una sola consulta
        queryset = Modulo.objects.select_related('id_categoria')
        
        if solo_activos:
            queryset = queryset.filter(estado=True)
            
        if not queryset.exists():
            return Response({"mensaje": "No hay módulos registrados"}, status=status.HTTP_204_NO_CONTENT)
        
        # Agrupar módulos por categoría
        modulos_por_categoria = defaultdict(list)
        
        for modulo in queryset:
            if modulo.id_categoria:
                # Serializar cada módulo
                serialized_modulo = ModuloReadSerializer(modulo).data
                
                # Agrupar por nombre de categoría
                categoria_nombre = modulo.id_categoria.nombre if hasattr(modulo.id_categoria, 'nombre') else str(modulo.id_categoria)
                modulos_por_categoria[categoria_nombre].append(serialized_modulo)
            
        # Convertir defaultdict a un diccionario normal para la respuesta
        resultado = dict(modulos_por_categoria)
        
        # Si no hay módulos con categoría, devolver mensaje específico
        if not resultado:
            return Response({"mensaje": "No hay módulos con categoría asignada"}, status=status.HTTP_200_OK)
        
        return Response(resultado, status=status.HTTP_200_OK)