import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semillero_backend.settings')
django.setup()

from datetime import date, timedelta
from oferta_academica.models import OfertaAcademica
from grupo.models import Grupo

def create_test_groups():
    print("Iniciando creación de grupos de prueba para diferentes periodos...")

    # 1. Crear o buscar un periodo actual (Activo)
    periodo_actual, created_act = OfertaAcademica.objects.get_or_create(
        nombre="Periodo 2026-Test-Actual",
        defaults={
            'fecha_inicio': date.today(),
            'estado': 'inscripcion'
        }
    )
    if not created_act:
        periodo_actual.estado = 'inscripcion'
        periodo_actual.save()
    print(f"-> Periodo Actual preparado: {periodo_actual.nombre} (ID: {periodo_actual.id_oferta_academica})")

    # 2. Crear o buscar un periodo anterior (Finalizado)
    periodo_anterior, created_ant = OfertaAcademica.objects.get_or_create(
        nombre="Periodo 2025-Test-Anterior",
        defaults={
            'fecha_inicio': date.today() - timedelta(days=365),
            'estado': 'finalizado'
        }
    )
    if not created_ant:
        periodo_anterior.estado = 'finalizado'
        periodo_anterior.save()
    print(f"-> Periodo Anterior preparado: {periodo_anterior.nombre} (ID: {periodo_anterior.id_oferta_academica})")

    # 3. Crear grupos en el periodo actual
    print("\nCreando grupos en periodo actual...")
    grupo1_actual, _ = Grupo.objects.get_or_create(
        nombre="Grupo Alpha",
        oferta_academica=periodo_actual
    )
    grupo2_actual, _ = Grupo.objects.get_or_create(
        nombre="Grupo Beta",
        oferta_academica=periodo_actual
    )
    print(f"✅ Creado: {grupo1_actual.nombre} en {grupo1_actual.oferta_academica.nombre}")
    print(f"✅ Creado: {grupo2_actual.nombre} en {grupo2_actual.oferta_academica.nombre}")

    # 4. Crear grupos (incluso con el mismo nombre) en el periodo anterior
    print("\nCreando grupos en periodo anterior...")
    grupo1_anterior, _ = Grupo.objects.get_or_create(
        nombre="Grupo Alpha", # Mismo nombre que el actual
        oferta_academica=periodo_anterior
    )
    grupo3_anterior, _ = Grupo.objects.get_or_create(
        nombre="Grupo Gamma",
        oferta_academica=periodo_anterior
    )
    print(f"✅ Creado: {grupo1_anterior.nombre} en {grupo1_anterior.oferta_academica.nombre}")
    print(f"✅ Creado: {grupo3_anterior.nombre} en {grupo3_anterior.oferta_academica.nombre}")
    
    print("\nResultados almacenados en Base de Datos de forma permanente.")
    
if __name__ == '__main__':
    create_test_groups()
