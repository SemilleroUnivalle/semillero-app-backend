from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Cerrar sesión",
        operation_description="Permite a un usuario cerrar sesión eliminando su token de autenticación",
        responses={
            status.HTTP_200_OK: "Logout exitoso",
            status.HTTP_401_UNAUTHORIZED: "No autorizado"
        }
    )
    def post(self, request):
        # Se elimina el token del usuario (al usar TokenAuthentication, request.auth corresponde al token)
        if request.auth:
            request.auth.delete()
        return Response({'detail': 'Logout exitoso'}, status=status.HTTP_200_OK)