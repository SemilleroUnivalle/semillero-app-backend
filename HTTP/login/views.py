from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class LoginView(APIView):
    # Permitir acceso sin autenticación (login no requiere token)
    authentication_classes = []
    permission_classes = []
    
    @swagger_auto_schema(
        operation_summary="Iniciar sesión",
        operation_description="Permite a un usuario iniciar sesión con su número de documento y contraseña",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'numero_documento': openapi.Schema(type=openapi.TYPE_STRING, description='Número de documento del usuario'),
                'contrasena': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del usuario')
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response('Inicio de sesión exitoso',
                                                openapi.Schema(type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'tipo_usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de usuario: administrador, profesor o estudiante'),
                                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID específico del usuario según su tipo')
                                                })),
            status.HTTP_400_BAD_REQUEST: "Falta numero_documento o contrasena",
            status.HTTP_401_UNAUTHORIZED: "Credenciales inválidas"
        }
    )
    def post(self, request):
        numero_documento = request.data.get('numero_documento')
        contrasena = request.data.get('contrasena')

        if not numero_documento or not contrasena:
            return Response({'detail': 'Falta numero_documento o contrasena'}, status=status.HTTP_400_BAD_REQUEST)

        # Usaremos el número de documento como username
        user = authenticate(username=numero_documento, password=contrasena)
        
        if user is None:
            return Response({'detail': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        
        # Obtener el ID específico según el tipo de usuario
        user_id = None
        tipo_usuario = user.user_type
        
        if tipo_usuario == 'administrador':
            try:
                from administrador.models import Administrador
                admin = Administrador.objects.get(numero_documento=numero_documento)
                user_id = admin.id_administrador
            except Exception as e:
                print(f"Error al buscar administrador: {str(e)}")
        elif tipo_usuario == 'profesor':
            try:
                from profesor.models import Profesor
                profesor = Profesor.objects.get(numero_documento=numero_documento)
                user_id = profesor.id
            except Exception as e:
                print(f"Error al buscar profesor: {str(e)}")
        elif tipo_usuario == 'estudiante':
            try:
                from estudiante.models import Estudiante
                estudiante = Estudiante.objects.get(numero_documento=numero_documento)
                user_id = estudiante.id_estudiante
            except Exception as e:
                print(f"Error al buscar estudiante: {str(e)}")
        elif tipo_usuario == 'monitor_academico':
            try:
                from monitor_academico.models import MonitorAcademico
                monitor_academico = MonitorAcademico.objects.get(numero_documento=numero_documento)
                user_id = monitor_academico.id
            except Exception as e:
                print(f"Error al buscar el monitor academico: {str(e)}")
        elif tipo_usuario == 'monitor_administrativo':
            try:
                from monitor_administrativo.models import MonitorAdministrativo
                monitor_administrativo = MonitorAdministrativo.objects.get(numero_documento=numero_documento)
                user_id = monitor_administrativo.id
            except Exception as e:
                print(f"Error al buscar el monitor administrativo: {str(e)}")
        
        # Devolver token, tipo de usuario y el ID específico
        return Response({
            'token': token.key,
            'tipo_usuario': tipo_usuario,
            'id': user_id
        }, status=status.HTTP_200_OK)
