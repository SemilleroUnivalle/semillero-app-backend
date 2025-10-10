#!/usr/bin/env python3
"""
Script para crear N usuarios (CustomUser) y Profesor asociados,
subir archivos (varios pdfs e imagen) usando la configuración de almacenamiento
de Django (local o S3) y evitando estados parciales con transacciones.

Ejecutar desde la raíz del proyecto Django con:
    python manage.py shell < crear_profesores_con_usuarios.py

Ajusta la sección "Configuración" más abajo para adaptar rutas, N, y opciones.
"""
import os
import random
from datetime import datetime, timedelta

from django.core.files import File
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model

from monitor_academico.models import MonitorAcademico


# Intentar importar Modulo si existe (opcional). Si no existe, lo ignoramos.
modulo_instance = None
modulo_lookup = None  # ajustar a id, slug o criterio si se desea enlazar un módulo, ejemplo: {'pk': 1} o {'slug': 'matematicas'}
if modulo_lookup:
    try:
        from modulo.models import Modulo  # ajustar path si corresponde
        modulo_qs = Modulo.objects.filter(**modulo_lookup)
        modulo_instance = modulo_qs.first() if modulo_qs.exists() else None
        if modulo_instance is None:
            print(f"AVISO: No se encontró Modulo con {modulo_lookup}. Se creará profesor sin modulo asignado.")
    except Exception:
        print("AVISO: No se pudo importar Modulo o no existe el app 'modulo'. Se creará profesor sin modulo asignado.")

# Configuración: ajustar según necesidad
N = 1  # Cantidad de profesores a crear
pk_inicio = 1
user_inicio = 1
numero_documento_inicio = 3000

# Archivos base (deben existir en base_dir) - nombres de ejemplo
base_dir = "/app/fixtures/documentos_profesor"
doc_id_base = "documento_identidad.pdf"
rut_base = "rut.pdf"
cert_bancario_base = "certificado_bancario.pdf"
d10_base = "d10.pdf"
tabulado_base = "tabulado.pdf"
estado_mat_financiera_base = "estado_mat_financiera.pdf"
foto_base = "foto.png"

# Contraseña en texto plano para los usuarios creados
contrasena_plain = "prueba123"
# Si tu modelo Profesor guarda el hash en un campo 'contrasena', manténlo aquí; si no, puedes dejarlo vacío.
contrasena_hash = "pbkdf2_sha256$720000$7x2oLNwzmTt8$6E8Vg0K+6F3kq9vP0gE3AqzUu8LqQJwQvG+m9Fq4n4Q="

# Datos aleatorios de ejemplo
nombres = [
    "Ana", "Carlos", "Luisa", "Juan", "María", "Santiago", "Andrea", "Valeria",
    "Esteban", "Camila", "Sofía", "Pedro", "Laura", "Felipe", "Juliana", "Mateo"
]
apellidos = [
    "Gómez", "Martínez", "Torres", "Pérez", "López", "Ramírez", "Castaño", "Rodríguez",
    "Moreno", "Jiménez", "Romero", "Vargas", "Suárez", "Navarro", "Cárdenas", "Muñoz"
]
ciudades = ["Cali", "Palmira", "Jamundí", "Yumbo", "Buga", "Tuluá", "Candelaria"]
epss = ["Sura", "Coomeva", "Nueva EPS"]
tipos_documento = ["CC", "TI"]
generos = ["Femenino", "Masculino", "Otro"]
comunas = [str(i) for i in range(1, 14)]
areas_desempeno = ["Matemáticas", "Lenguaje", "Ciencias", "Inglés", "Educación Física"]
semestres = ["5", "6", "7", "8"]

UserModel = get_user_model()

def ensure_file(path):
    """Comprueba si existe el archivo y devuelve True/False"""
    if not os.path.exists(path):
        print(f"AVISO: archivo no encontrado: {path}. Se omitirá adjunto para este registro.")
        return False
    return True

def create_user_safe(username, email, first_name, last_name, password):
    """
    Crea un usuario usando create_user si está disponible; si no usa set_password.
    Devuelve el usuario creado o existente.
    """
    try:
        # Intentar crear con create_user (maneja hashing y defaults)
        if hasattr(UserModel.objects, "create_user"):
            user = UserModel.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type="monitor_academico"
            )
        else:
            user = UserModel(username=username, email=email, first_name=first_name, last_name=last_name, user_type="monitor_academico")
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
        tipo_documento = random.choice(tipos_documento)
        genero = random.choice(generos)
        comuna = random.choice(comunas)
        fecha_base = datetime.strptime("1980-01-01", "%Y-%m-%d")
        fecha_nacimiento = (fecha_base + timedelta(days=random.randint(0, 40*365))).date()
        telefono_fijo = f"6{random.randint(1000000,9999999)}"
        celular = f"3{random.randint(1000000000,1999999999)}"[:10]
        departamento_residencia = "Valle del Cauca"
        direccion_residencia = f"Calle {random.randint(1, 300)} #{random.randint(1,50)}-{random.randint(1,99)}"
        area_desempeno = random.choice(areas_desempeno)
        semestre = random.choice(semestres)

        username = numero_documento  # usar número de documento como username

        # Rutas a archivos base
        doc_id_path = os.path.join(base_dir, doc_id_base)
        rut_path = os.path.join(base_dir, rut_base)
        cert_bancario_path = os.path.join(base_dir, cert_bancario_base)
        d10_path = os.path.join(base_dir, d10_base)
        tabulado_path = os.path.join(base_dir, tabulado_base)
        estado_mat_financiera_path = os.path.join(base_dir, estado_mat_financiera_base)
        foto_path = os.path.join(base_dir, foto_base)

        # Crear usuario y profesor dentro de transacción para evitar estados parciales
        try:
            with transaction.atomic():
                user = create_user_safe(username=username, email=email, first_name=nombre, last_name=apellido, password=contrasena_plain)

                # Construir instancia Profesor (sin archivos aún)
                monitor_academico = MonitorAcademico(
                    user=user,
                    nombre=nombre,
                    apellido=apellido,
                    contrasena=contrasena_hash,  # ajustar según tu modelo
                    numero_documento=numero_documento,
                    email=email,
                    ciudad_residencia=ciudad,
                    eps=eps,
                    tipo_documento=tipo_documento,
                    genero=genero,
                    fecha_nacimiento=fecha_nacimiento,
                    telefono_fijo=telefono_fijo,
                    celular=celular,
                    departamento_residencia=departamento_residencia,
                    comuna_residencia=comuna,
                    direccion_residencia=direccion_residencia,
                    area_desempeño=area_desempeno,
                    semestre=semestre,
                )

                # Si se encontró una instancia de modulo, asignarla
                if modulo_instance is not None:
                    try:
                        monitor_academico.modulo = modulo_instance
                    except Exception:
                        # En caso de que el campo tenga otro nombre o no exista, lo ignoramos
                        print("AVISO: No se pudo asignar 'modulo' al Profesor (campo ausente o nombre distinto).")

                # Adjuntar archivos si existen (se usa save=False para guardar todo junto)
                if ensure_file(doc_id_path):
                    with open(doc_id_path, "rb") as f:
                        monitor_academico.documento_identidad_pdf.save(f"{pk}_{doc_id_base}", File(f), save=False)

                if ensure_file(rut_path):
                    with open(rut_path, "rb") as f:
                        monitor_academico.rut_pdf.save(f"{pk}_{rut_base}", File(f), save=False)

                if ensure_file(cert_bancario_path):
                    with open(cert_bancario_path, "rb") as f:
                        monitor_academico.certificado_bancario_pdf.save(f"{pk}_{cert_bancario_base}", File(f), save=False)

                if ensure_file(d10_path):
                    with open(d10_path, "rb") as f:
                        monitor_academico.d10_pdf.save(f"{pk}_{d10_base}", File(f), save=False)

                if ensure_file(tabulado_path):
                    with open(tabulado_path, "rb") as f:
                        monitor_academico.tabulado_pdf.save(f"{pk}_{tabulado_base}", File(f), save=False)

                if ensure_file(estado_mat_financiera_path):
                    with open(estado_mat_financiera_path, "rb") as f:
                        monitor_academico.estado_mat_financiera_pdf.save(f"{pk}_{estado_mat_financiera_base}", File(f), save=False)

                if ensure_file(foto_path):
                    with open(foto_path, "rb") as f:
                        monitor_academico.foto.save(f"{pk}_{foto_base}", File(f), save=False)

                # Guardar instancia Profesor (y con ello las relaciones a archivos)
                monitor_academico.save()
                created += 1
                print(f"{i+1}/{N}: Usuario '{username}' y Monitor Academico '{nombre} {apellido}' creados (PK Monitor: {monitor_academico.pk}).")
        except Exception as e:
            print(f"ERROR creando registro {i+1} (numero_documento={numero_documento}): {e}")
            # continuar con los siguientes registros

    print(f"Fin: {created}/{N} monitores creados con usuarios asociados.")

if __name__ == "__main__":
    main()