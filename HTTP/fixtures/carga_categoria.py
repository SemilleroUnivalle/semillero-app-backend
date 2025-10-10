#!/usr/bin/env python3
"""
Script para crear/actualizar las 3 categorías básicas:
  - Semillero
  - NAS
  - Formacion Docente

Uso:
    Desde la raíz del proyecto Django:
        python manage.py shell < crear_categorias.py

Ajusta el import si tu app/modelo Categoria está en otra ubicación.
"""
from django.db import transaction, IntegrityError

from categoria.models import Categoria

# Lista fija de categorías a crear
CATEGORIAS = [
    {"nombre": "Semillero", "estado": True},
    {"nombre": "NAS", "estado": True},
    {"nombre": "Formacion Docente", "estado": True},
]

def main():
    created = 0
    updated = 0
    for idx, item in enumerate(CATEGORIAS, start=1):
        nombre = item["nombre"]
        estado = item.get("estado", True)
        try:
            with transaction.atomic():
                obj, was_created = Categoria.objects.get_or_create(
                    nombre=nombre,
                    defaults={"estado": estado}
                )

                if not was_created:
                    # Actualizar estado si es distinto
                    if obj.estado != estado:
                        obj.estado = estado
                        obj.save()
                        updated += 1

                if was_created:
                    created += 1
                    print(f"{idx}: Categoria creada: '{nombre}' (pk={obj.pk})")
                else:
                    print(f"{idx}: Categoria existente: '{nombre}' (pk={obj.pk})")

        except IntegrityError as e:
            print(f"ERROR de integridad creando/actualizando '{nombre}': {e}")
        except Exception as e:
            print(f"ERROR creando/actualizando '{nombre}': {e}")

    print(f"Fin: {created} creadas, {updated} actualizadas ({len(CATEGORIAS)} procesadas).")

if __name__ == "__main__":
    main()