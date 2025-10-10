#!/usr/bin/env python3
"""
Script para crear N usuarios (CustomUser) y Estudiante asociados,
subir archivos (imagen y pdf) usando la configuración de almacenamiento
de Django (local o S3) y evitar el error de integridad por user_id nulo.

Ejecutar desde la raíz del proyecto Django con:
    python manage.py shell < crear_estudiantes_con_usuarios.py
"""

import os
import random
from datetime import datetime, timedelta

from django.core.files import File
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model

from estudiante.models import Estudiante

# Configuración: ajustar según necesidad
N = 10  # Cantidad de estudiantes a crear
pk_inicio = 1
user_inicio = 1
numero_documento_inicio = 110

# Archivos base (deben existir en base_dir)
base_dir = "/app/fixtures/documentos"
doc_id_base = "documento_identidad.pdf"
foto_base = "foto.png"

# Contraseña en texto plano para los usuarios creados (se aplicará con set_password/create_user)
contrasena_plain = "prueba123"
# Si quieres guardar también el hash en el campo 'contrasena' del Estudiante, puedes mantenerlo:
contrasena_hash = "pbkdf2_sha256$720000$7x2oLNwzmTt8$6E8Vg0K+6F3kq9vP0gE3AqzUu8LqQJwQvG+m9Fq4n4Q="

# Datos aleatorios
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

UserModel = get_user_model()

def ensure_file(path):
    """Comprueba si existe el archivo y devuelve True/False"""
    if not os.path.exists(path):
        print(f"AVISO: archivo no encontrado: {path}. Se omitirá adjunto para este registro.")
        return False
    return True

def create_user_safe(username, email, first_name, last_name, password):
    """
    Crea un usuario usando create_user si está disponible, si no usa set_password.
    Devuelve el usuario creado o existente.
    """
    try:
        # Intentar crear con create_user (maneja hashing)
        if hasattr(UserModel.objects, "create_user"):
            user = UserModel.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
        else:
            user = UserModel(username=username, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
    except IntegrityError:
        # Si ya existe (por ejemplo), intentar obtenerlo
        try:
            user = UserModel.objects.get(username=username)
            print(f"Nota: usuario existente obtenido: {username}")
        except UserModel.DoesNotExist:
            raise
    return user

def main():
    created = 0
    for i in range(N):
        pk = pk_inicio + i
        user_idx = user_inicio + i
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
        fecha_nacimiento = (fecha_base + timedelta(days=random.randint(0, 6*365))).date()
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

        username = numero_documento  # usar el número de documento como username

        # Crear usuario y estudiante dentro de transacción para evitar estados parciales
        try:
            with transaction.atomic():
                usuario = create_user_safe(username=username, email=email, first_name=nombre, last_name=apellido, password=contrasena_plain)

                # Construir instancia Estudiante
                estudiante = Estudiante(
                    user=usuario,
                    nombre=nombre,
                    apellido=apellido,
                    contrasena=contrasena_hash,  # si tu modelo guarda el hash, puedes dejarlo; si no, ignóralo
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
                    fecha_nacimiento=fecha_nacimiento,
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

                # Adjuntar archivos si existen
                doc_id_path = os.path.join(base_dir, doc_id_base)
                foto_path = os.path.join(base_dir, foto_base)

                if ensure_file(doc_id_path):
                    with open(doc_id_path, 'rb') as f:
                        # se usa save=False para guardar todos los campos juntos al final
                        estudiante.documento_identidad.save(f"{pk}_{doc_id_base}", File(f), save=False)

                if ensure_file(foto_path):
                    with open(foto_path, 'rb') as f:
                        estudiante.foto.save(f"{pk}_{foto_base}", File(f), save=False)

                estudiante.save()
                created += 1
                print(f"{i+1}/{N}: Usuario '{username}' y Estudiante '{nombre} {apellido}' creados (PK Estudiante: {estudiante.pk}).")
        except Exception as e:
            print(f"ERROR creando registro {i+1} (numero_documento={numero_documento}): {e}")
            # continuar con los siguientes registros

    print(f"Fin: {created}/{N} estudiantes creados con usuarios asociados.")

if __name__ == "__main__":
    main()