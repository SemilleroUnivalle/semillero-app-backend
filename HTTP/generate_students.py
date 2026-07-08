import os
import django
import random
import string
from datetime import datetime, date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "semillero_backend.settings")
django.setup()

from django.contrib.auth import get_user_model
from estudiante.models import Estudiante
from acudiente.models import Acudiente
from inscripcion.models import Inscripcion
from oferta_academica.models import OfertaAcademica
from modulo.models import Modulo

User = get_user_model()

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_number(length=10):
    return ''.join(random.choices(string.digits, k=length))

def run():
    oferta = OfertaAcademica.objects.filter(nombre__icontains='2026-2').first()
    if not oferta:
        print("No se encontró la oferta 2026-2")
        ofertas = OfertaAcademica.objects.all()
        print("Ofertas disponibles:", [o.nombre for o in ofertas])
        return

    modulos = list(Modulo.objects.all())

    
    nombres = ["Andres", "Carlos", "Maria", "Laura", "Juan", "Pedro", "Luisa", "Ana", "Jorge", "Sofia", "Diego", "Luis", "Valentina", "Camila", "Lucia", "Julian", "Gabriel", "Samuel", "Sara", "Isabella", "Mateo", "Mariana", "Emilio", "Antonia", "Sebastian"]
    apellidos = ["Gomez", "Perez", "Rodriguez", "Fernandez", "Lopez", "Martinez", "Gonzalez", "Diaz", "Castro", "Ortiz", "Silva", "Vargas", "Ramirez", "Cruz", "Guzman", "Alvarez", "Mendoza", "Rojas", "Herrera", "Medina", "Romero", "Torres"]

    created_count = 0
    for i in range(50):
        # 1. Crear Acudiente
        acu_doc = str(random.randint(10000000, 99999999))
        acudiente = Acudiente.objects.create(
            numero_documento=acu_doc,
            nombre=random.choice(nombres),
            apellido=random.choice(apellidos),
            parentesco=random.choice(["Padre", "Madre", "Tío", "Abuela", "Abuelo"]),
            telefono_fijo=random_number(7),
            celular="3" + random_number(9),
            correo_electronico=f"acu{acu_doc}@ejemplo.com",
            lugar_expedicion=random.choice(["Cali", "Palmira", "Buga", "Yumbo", "Jamundi", "Yumbo"])
        )

        # 2. Crear User
        est_doc = str(random.randint(1000000000, 1999999999))
        email = f"est{est_doc}@ejemplo.com"
        user = User.objects.create_user(
            username=est_doc,
            email=email,
            password="password123",
            first_name=random.choice(nombres),
            last_name=random.choice(apellidos),
            user_type="estudiante"
        )

        # 3. Crear Estudiante
        estudiante = Estudiante.objects.create(
            user=user,
            nombre=user.first_name,
            apellido=user.last_name,
            numero_documento=est_doc,
            email=email,
            acudiente=acudiente,
            ciudad_residencia="Cali",
            eps=random.choice(["Sura", "Sanitas", "Coomeva", "Emssanar", "SOS", "Asmet Salud", "Nueva EPS", "Salud Total"]),
            grado=random.choice(["6", "7", "8", "9", "10", "11"]),
            colegio="Colegio Principal " + random_string(3).upper(),
            tipo_documento="TI",
            genero=random.choice(["Masculino", "Femenino", "Otro", "Prefiero no decir"]),
            fecha_nacimiento=date(random.randint(2005, 2012), random.randint(1, 12), random.randint(1, 28)),
            telefono_fijo=random_number(7),
            celular="3" + random_number(9),
            departamento_residencia="Valle del Cauca",
            comuna_residencia=str(random.randint(1, 22)),
            direccion_residencia=f"Carrera {random.randint(1,100)} # {random.randint(1,100)}-{random.randint(1,100)}",
            estamento="Estudiante Regular",
            discapacidad=False,
            estado="Revisado"
        )

        # 4. Crear Inscripcion
        modulo = random.choice(modulos) if modulos else None
        
        Inscripcion.objects.create(
            id_estudiante=estudiante,
            id_modulo=modulo,
            oferta_academica=oferta,
            tipo_vinculacion=random.choice(["Estudiante Regular", "Renovacion", "Inscripcion Nueva"]),
            terminos=True,
            estado=random.choice(["Aceptado", "En proceso", "Revisado"])
        )
        created_count += 1

    print(f"[{created_count}] Estudiantes inscritos correctamente para {oferta.nombre}")

if __name__ == '__main__':
    run()
