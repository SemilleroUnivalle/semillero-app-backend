from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Llama al manejador de excepciones predeterminado primero
    response = exception_handler(exc, context)
    
    # Personaliza mensajes de error de permisos
    if response is not None and response.status_code == status.HTTP_403_FORBIDDEN:
        response.data = {
            "detail": "No tienes permisos suficientes para realizar esta acción.",
            "code": "permiso denegado"
        }
        
    return response