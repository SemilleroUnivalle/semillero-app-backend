from rest_framework.authentication import TokenAuthentication

class BearerTokenAuthentication(TokenAuthentication):
    """
    Extiende TokenAuthentication para aceptar la palabra clave 'Bearer'
    en el encabezado de autorización, lo cual es estándar en muchos clientes REST.
    """
    keyword = 'Bearer'
