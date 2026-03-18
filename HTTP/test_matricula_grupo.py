import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semillero_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate
from inscripcion.views import InscripcionViewSet

def test_matricula_grupo():
    factory = APIRequestFactory()
    request = factory.get('/inscripcion/matricula-grupo/')
    
    User = get_user_model()
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.first()
        
    force_authenticate(request, user=admin_user)
    
    view = InscripcionViewSet.as_view({'get': 'matricula_grupo'})
    response = view(request)
    
    print(f"Status: {response.status_code}")
    import json
    # Print the first 2 groups to see what it looks like
    print(json.dumps(response.data[:2], indent=2))

if __name__ == '__main__':
    test_matricula_grupo()
