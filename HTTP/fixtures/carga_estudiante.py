import os
import random
from datetime import datetime, timedelta
from django.core.files import File
from estudiante.models import Estudiante

N = 10  # Cantidad de estudiantes a crear
pk_inicio = 2
user_inicio = 2
numero_documento_inicio = 101

nombres = [
    "Ana", "Carlos", "Luisa", "Juan", "Maria", "Santiago", "Andrea", "Valeria",
    "Esteban", "Camila", "Sofia", "Pedro", "Laura", "Felipe", "Juliana", "Mateo"
]
apellidos = [
    "Gomez", "Martinez", "Torres", "Perez", "López", "Ramirez", "Castaño", "Rodriguez",
    "Moreno", "Jimenez", "Romero", "Vargas", "Suarez", "Navarro", "Cardenas", "Muñoz"
]
ciudades = ["Cali", "Palmira", "Jamundi", "Yumbo", "Buga", "Tuluá", "Candelaria"]
epss = ["Sura", "Coomeva", "Nueva EPS"]
colegios = ["Colegio Central", "Instituto Sur", "Liceo Moderno", "Colegio Norte"]
tipos_documento = ["CC", "TI"]
generos = ["Femenino", "Masculino"]
estamentos = ["publico", "privado"]
comunas = [str(i) for i in range(1, 14)]

contrasena_hash = "pbkdf2_sha256$720000$7x2oLNwzmTt8$6E8Vg0K+6F3kq9vP0gE3AqzUu8LqQJwQvG+m9Fq4n4Q="
base_dir = "/app/fixtures/documentos"
doc_id_base = "foto.png"
foto_base = "documento_identidad.pdf"

for i in range(N):
    pk = pk_inicio + i
    user = user_inicio + i
    numero_documento = str(numero_documento_inicio + i)
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    email = f"{nombre.lower()}.{apellido.lower()}{pk}@email.com"
    ciudad = random.choice(ciudades)
    eps = random.choice(epss)
    colegio = random.choice(colegios)
    tipo_documento = random.choice(tipos_documento)
    genero = random.choice(generos)
    estamento = random.choice(estamentos)
    comuna = random.choice(comunas)
    fecha_base = datetime.strptime("2002-01-01", "%Y-%m-%d")
    fecha_nacimiento = fecha_base + timedelta(days=random.randint(0, 6*365))
    telefono_fijo = f"31{random.randint(10000,99999)}"
    celular = f"32{random.randint(10000000,99999999)}"
    is_active = True
    acudiente = random.randint(1, 10)
    grado = str(random.randint(1, 11))
    departamento_residencia = "Valle del cauca"
    direccion_residencia = f"Calle {random.randint(1, 30)} #{random.randint(1,50)}-{random.randint(1,99)}"
    discapacidad = random.random() < 0.1
    if discapacidad:
        tipo_discapacidad = random.choice(["Auditiva", "Visual", "Motora"])
        descripcion_discapacidad = f"Discapacidad {tipo_discapacidad.lower()}"
    else:
        tipo_discapacidad = "Ninguna"
        descripcion_discapacidad = "Ninguna"

    estudiante = Estudiante(
        nombre=nombre,
        apellido=apellido,
        contrasena=contrasena_hash,
        numero_documento=numero_documento,
        email=email,
        is_active=is_active,
        acudiente_id=acudiente,
        ciudad_residencia=ciudad,
        eps=eps,
        grado=grado,
        colegio=colegio,
        tipo_documento=tipo_documento,
        genero=genero,
        fecha_nacimiento=fecha_nacimiento.strftime("%Y-%m-%d"),
        telefono_fijo=telefono_fijo,
        celular=celular,
        departamento_residencia=departamento_residencia,
        comuna_residencia=comuna,
        direccion_residencia=direccion_residencia,
        estamento=estamento,
        discapacidad=discapacidad,
        tipo_discapacidad=tipo_discapacidad,
        descripcion_discapacidad=descripcion_discapacidad
    )

    # Adjuntar archivos
    doc_id_path = os.path.join(base_dir, doc_id_base)
    foto_path = os.path.join(base_dir, foto_base)

    with open(doc_id_path, 'rb') as f:
        estudiante.documento_identidad.save(f"{pk}_{doc_id_base}", File(f), save=False)
    with open(foto_path, 'rb') as f:
        estudiante.foto.save(f"{pk}_{foto_base}", File(f), save=False)

    estudiante.save()
    print(f"{i+1}/{N}: Estudiante {estudiante.nombre} {estudiante.apellido} creado y archivos subidos en S3.")

print("Todos los estudiantes han sido creados exitosamente.")