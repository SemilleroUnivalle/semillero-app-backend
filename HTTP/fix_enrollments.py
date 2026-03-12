import os
import django
from django.db import transaction

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semillero_backend.settings')
django.setup()

from estudiante.models import Estudiante
from oferta_academica.models import OfertaAcademica
from modulo.models import Modulo
from inscripcion.models import Inscripcion

def populate_exact_enrollments():
    with transaction.atomic():
        # 1. Obtener periodos
        p2026_1 = OfertaAcademica.objects.get(nombre="2026-1")
        p2026_2 = OfertaAcademica.objects.get(nombre="2026-2")
        
        # 2. Limpiar inscripciones previas de estos periodos
        print(f"Limpiando inscripciones previas de {p2026_1.nombre} y {p2026_2.nombre}...")
        Inscripcion.objects.filter(oferta_academica__in=[p2026_1, p2026_2]).delete()

        # 3. Obtener módulos para inscribir
        mats = list(Modulo.objects.all())
        if not mats:
            print("❌ No hay módulos disponibles. Operación abortada.")
            return

        # 4. Inscribir 90 en 2026-1
        # Usamos los estudiantes que NO son del futuro (los 100 originales)
        estudiantes_base = Estudiante.objects.filter(numero_documento__regex=r'^\d+$')[:90]
        print(f"Inscribiendo 90 estudiantes en {p2026_1.nombre}...")
        for i, est in enumerate(estudiantes_base):
            mod = mats[i % len(mats)]
            oc = mod.id_oferta_categoria.first()
            Inscripcion.objects.create(
                id_estudiante=est,
                id_modulo=mod,
                oferta_academica=p2026_1,
                id_oferta_categoria=oc,
                tipo_vinculacion='Regular',
                terminos=True,
                estado='No revisado'
            )

        # 5. Inscribir 100 en 2026-2
        # Usamos los estudiantes del futuro
        estudiantes_futuro = Estudiante.objects.filter(numero_documento__startswith='FUTURE_')[:100]
        print(f"Inscribiendo 100 estudiantes en {p2026_2.nombre}...")
        for i, est in enumerate(estudiantes_futuro):
            mod = mats[i % len(mats)]
            oc = mod.id_oferta_categoria.first()
            Inscripcion.objects.create(
                id_estudiante=est,
                id_modulo=mod,
                oferta_academica=p2026_2,
                id_oferta_categoria=oc,
                tipo_vinculacion='Regular',
                terminos=True,
                estado='No revisado'
            )

        print("\n✅ PROCESO COMPLETADO EXITOSAMENTE")
        print(f"- 2026-1: {Inscripcion.objects.filter(oferta_academica=p2026_1).count()} inscritos")
        print(f"- 2026-2: {Inscripcion.objects.filter(oferta_academica=p2026_2).count()} inscritos")

if __name__ == "__main__":
    populate_exact_enrollments()
