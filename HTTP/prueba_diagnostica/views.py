from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django.core.exceptions import ValidationError

# Documentación
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Modelos
from .models import PruebaDiagnostica, PreguntaDiagnostica, RespuestaDiagnostica
from modulo.models import Modulo

# Serializadores
from .serializers import (
    PruebaDiagnosticaReadSerializer,
    PruebaDiagnosticaWriteSerializer,
    PreguntaDiagnosticaReadSerializer,
    PreguntaDiagnosticaWriteSerializer,
    RespuestaDiagnosticaSerializer,
    RespuestaDiagnosticaWriteSerializer,
    PreguntaConRespuestasSerializer
)

# Autenticación y Permisos
from rest_framework.permissions import IsAuthenticated
from cuenta.permissions import IsAdministrador, IsProfesorOrAdministrador


class PruebaDiagnosticaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar Pruebas Diagnósticas.
    
    Permite listar, crear, actualizar y eliminar pruebas diagnósticas.
    """
    queryset = PruebaDiagnostica.objects.all()
    permission_classes = [IsAuthenticated, IsAdministrador]

    def get_serializer_class(self):
        """
        Usa el serializador correcto según el método:
        - Para GET: PruebaDiagnosticaReadSerializer con relaciones completas
        - Para POST, PUT, PATCH: PruebaDiagnosticaWriteSerializer
        """
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return PruebaDiagnosticaWriteSerializer
        return PruebaDiagnosticaReadSerializer

    @swagger_auto_schema(
        operation_summary="Listar todas las pruebas diagnósticas",
        operation_description="Retorna todas las pruebas diagnósticas registradas"
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Crear una prueba diagnóstica",
        operation_description="Crea una nueva prueba diagnóstica asociada a un módulo",
        request_body=PruebaDiagnosticaWriteSerializer,
        responses={
            status.HTTP_201_CREATED: PruebaDiagnosticaReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            instance = serializer.instance
            read_serializer = PruebaDiagnosticaReadSerializer(instance)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detalle": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Obtener una prueba diagnóstica específica",
        operation_description="Retorna los detalles de una prueba diagnóstica por su ID, incluyendo todas sus preguntas"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Actualizar una prueba diagnóstica",
        operation_description="Actualiza todos los campos de una prueba diagnóstica existente",
        request_body=PruebaDiagnosticaWriteSerializer,
        responses={
            status.HTTP_200_OK: PruebaDiagnosticaReadSerializer,
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
            read_serializer = PruebaDiagnosticaReadSerializer(instance)
            return Response(read_serializer.data)
        except ValidationError as e:
            return Response({"detalle": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una prueba diagnóstica",
        operation_description="Actualiza uno o más campos de una prueba diagnóstica existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Eliminar una prueba diagnóstica",
        operation_description="Elimina permanentemente una prueba diagnóstica y todas sus preguntas"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Listar pruebas por módulo",
        operation_description="Retorna todas las pruebas diagnósticas de un módulo específico",
        manual_parameters=[
            openapi.Parameter(
                'id_modulo',
                openapi.IN_QUERY,
                description="ID del módulo",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'], url_path='por-modulo')
    def por_modulo(self, request):
        """
        Endpoint para listar las pruebas diagnósticas de un módulo específico.
        """
        id_modulo = request.query_params.get('id_modulo')
        
        if not id_modulo:
            return Response(
                {"detalle": "Debe proporcionar el parámetro 'id_modulo'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            modulo = Modulo.objects.get(id_modulo=id_modulo)
        except Modulo.DoesNotExist:
            return Response(
                {"detalle": "Módulo no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        pruebas = PruebaDiagnostica.objects.filter(id_modulo=modulo, estado=True)
        
        if not pruebas.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        serializer = PruebaDiagnosticaReadSerializer(pruebas, many=True)
        return Response(serializer.data)


class PreguntaDiagnosticaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar Preguntas Diagnósticas.
    
    Permite listar, crear, actualizar y eliminar preguntas diagnósticas.
    """
    queryset = PreguntaDiagnostica.objects.all()
    permission_classes = [IsAuthenticated, IsAdministrador]

    def get_serializer_class(self):
        """
        Usa el serializador correcto según la acción:
        - Para crear_con_respuestas: PreguntaConRespuestasSerializer
        - Para GET: PreguntaDiagnosticaReadSerializer
        - Para POST, PUT, PATCH: PreguntaDiagnosticaWriteSerializer
        """
        if self.action == 'crear_con_respuestas':
            return PreguntaConRespuestasSerializer
        elif self.request.method in ['POST', 'PUT', 'PATCH']:
            return PreguntaDiagnosticaWriteSerializer
        return PreguntaDiagnosticaReadSerializer

    @swagger_auto_schema(
        operation_summary="Listar todas las preguntas diagnósticas",
        operation_description="Retorna todas las preguntas diagnósticas con sus respuestas"
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Crear una pregunta diagnóstica",
        operation_description="Crea una nueva pregunta diagnóstica (sin respuestas). Use 'crear-con-respuestas' para crear pregunta y respuestas juntas.",
        request_body=PreguntaDiagnosticaWriteSerializer,
        responses={
            status.HTTP_201_CREATED: PreguntaDiagnosticaReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            instance = serializer.instance
            read_serializer = PreguntaDiagnosticaReadSerializer(instance)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detalle": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Crear pregunta con respuestas",
        operation_description="Crea una pregunta diagnóstica junto con sus respuestas en una sola operación",
        request_body=PreguntaConRespuestasSerializer,
        responses={
            status.HTTP_201_CREATED: PreguntaDiagnosticaReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    @action(detail=False, methods=['post'], url_path='crear-con-respuestas')
    def crear_con_respuestas(self, request):
        """
        Endpoint para crear una pregunta con sus respuestas en una sola operación.
        
        Formato esperado:
        {
            "id_prueba": 1,
            "texto_pregunta": "¿Cuál es la capital de Francia?",
            "tipo_pregunta": "multiple",
            "puntaje": 1.0,
            "orden": 1,
            "respuestas": [
                {"texto_respuesta": "París", "es_correcta": true},
                {"texto_respuesta": "Londres", "es_correcta": false},
                {"texto_respuesta": "Madrid", "es_correcta": false}
            ]
        }
        """
        serializer = PreguntaConRespuestasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                pregunta = serializer.save()
                read_serializer = PreguntaDiagnosticaReadSerializer(pregunta)
                return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detalle": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detalle": f"Error al crear pregunta: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_summary="Obtener una pregunta específica",
        operation_description="Retorna los detalles de una pregunta diagnóstica por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Actualizar una pregunta",
        operation_description="Actualiza todos los campos de una pregunta existente"
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_update(serializer)
            read_serializer = PreguntaDiagnosticaReadSerializer(instance)
            return Response(read_serializer.data)
        except ValidationError as e:
            return Response({"detalle": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una pregunta",
        operation_description="Actualiza uno o más campos de una pregunta existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Eliminar una pregunta",
        operation_description="Elimina permanentemente una pregunta y todas sus respuestas"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Listar preguntas por prueba",
        operation_description="Retorna todas las preguntas de una prueba diagnóstica específica",
        manual_parameters=[
            openapi.Parameter(
                'id_prueba',
                openapi.IN_QUERY,
                description="ID de la prueba diagnóstica",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'], url_path='por-prueba')
    def por_prueba(self, request):
        """
        Endpoint para listar las preguntas de una prueba diagnóstica específica.
        """
        id_prueba = request.query_params.get('id_prueba')
        
        if not id_prueba:
            return Response(
                {"detalle": "Debe proporcionar el parámetro 'id_prueba'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            prueba = PruebaDiagnostica.objects.get(id_prueba=id_prueba)
        except PruebaDiagnostica.DoesNotExist:
            return Response(
                {"detalle": "Prueba diagnóstica no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        preguntas = PreguntaDiagnostica.objects.filter(id_prueba=prueba, estado=True)
        
        if not preguntas.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        serializer = PreguntaDiagnosticaReadSerializer(preguntas, many=True)
        return Response(serializer.data)


class RespuestaDiagnosticaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar Respuestas Diagnósticas.
    
    Permite listar, crear, actualizar y eliminar respuestas diagnósticas.
    """
    queryset = RespuestaDiagnostica.objects.all()
    permission_classes = [IsAuthenticated, IsAdministrador]

    def get_serializer_class(self):
        """
        Usa el serializador correcto según el método.
        """
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return RespuestaDiagnosticaWriteSerializer
        return RespuestaDiagnosticaSerializer

    @swagger_auto_schema(
        operation_summary="Listar todas las respuestas",
        operation_description="Retorna todas las respuestas diagnósticas"
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Crear una respuesta",
        operation_description="Crea una nueva respuesta para una pregunta diagnóstica",
        request_body=RespuestaDiagnosticaWriteSerializer
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detalle": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Actualizar una respuesta",
        operation_description="Actualiza todos los campos de una respuesta existente"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una respuesta",
        operation_description="Actualiza uno o más campos de una respuesta existente"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Eliminar una respuesta",
        operation_description="Elimina permanentemente una respuesta"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
