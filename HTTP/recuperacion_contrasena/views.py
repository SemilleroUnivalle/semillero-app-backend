from django_rest_passwordreset.views import ResetPasswordRequestToken
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

@swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'numero_documento': openapi.Schema(type=openapi.TYPE_STRING, description='Número de documento del usuario'),
            },
        ),
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
        }
    )
class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    def post(self, request, *args, **kwargs):
        document_number = request.data.get("numero_documento")
        if not document_number:
            return Response({'error': 'Se requiere el número de documento.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=document_number)
        except User.DoesNotExist:
            # No reveles si el número existe o no: responde como si hubiera funcionado
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        # Ahora arma un request con el email del usuario y pásalo a la vista original
        mutable_data = request.data.copy()
        mutable_data['email'] = user.email
        request._full_data = mutable_data 
        return super().post(request, *args, **kwargs)