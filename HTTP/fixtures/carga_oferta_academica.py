#!/usr/bin/env python3
"""
Script para crear/actualizar Oferta Académica.

Uso:
    Desde la raíz del proyecto Django:
        python manage.py shell -c "exec(open('fixtures/carga_oferta_academica.py').read()); main()"
"""
from django.db import IntegrityError, transaction
from datetime import date

from oferta_academica.models import OfertaAcademica

# ---------------------- CONFIGURACIÓN ----------------------
# Datos de la oferta académica
OFERTA_DATA = {
    "nombre": "2025",
    "fecha_inicio": date(2025, 4, 23),
    "estado": True  # Activada por defecto
}
# -----------------------------------------------------------

def main():
    created = 0
    updated = 0
    
    try:
        with transaction.atomic():
            # Intentar obtener o crear
            oferta_obj, was_created = OfertaAcademica.objects.get_or_create(
                nombre=OFERTA_DATA["nombre"],
                defaults={
                    "fecha_inicio": OFERTA_DATA["fecha_inicio"],
                    "estado": OFERTA_DATA["estado"]
                }
            )

            # Si no fue creado, actualizar si es necesario
            if not was_created:
                changed = False
                if oferta_obj.fecha_inicio != OFERTA_DATA["fecha_inicio"]:
                    oferta_obj.fecha_inicio = OFERTA_DATA["fecha_inicio"]
                    changed = True
                if oferta_obj.estado != OFERTA_DATA["estado"]:
                    oferta_obj.estado = OFERTA_DATA["estado"]
                    changed = True
                if changed:
                    oferta_obj.save()
                    updated += 1

            if was_created:
                created += 1
                print(f"Oferta Académica creada: '{oferta_obj.nombre}' (pk={oferta_obj.pk})")
            else:
                print(f"Oferta Académica existente: '{oferta_obj.nombre}' (pk={oferta_obj.pk})")

    except IntegrityError as e:
        print(f"ERROR de integridad creando/actualizando Oferta Académica: {e}")
    except Exception as e:
        print(f"ERROR creando/actualizando Oferta Académica: {e}")

    print(f"Fin: {created} creadas, {updated} actualizadas.")

if __name__ == "__main__":
    main()
