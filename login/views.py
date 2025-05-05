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
        operation_description="Permite a un estudiante iniciar sesión con su número de documento y contraseña",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'numero_documento': openapi.Schema(type=openapi.TYPE_STRING, description='Número de documento del estudiante'),
                'contrasena': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del estudiante')
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response('Inicio de sesión exitoso',
                                                  openapi.Schema(type=openapi.TYPE_OBJECT,
                                                  properties={'token': openapi.Schema(type=openapi.TYPE_STRING)})),
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
        return Response({'token': token.key, 'tipo_usuario':user.user_type}, status=status.HTTP_200_OK)
