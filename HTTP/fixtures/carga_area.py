#!/usr/bin/env python3
"""
Script para crear/actualizar registros Area usando la configuración de
almacenamiento de Django (local o S3).

Uso:
    Desde la raíz del proyecto Django:
        python manage.py shell < crear_areas.py

Ajusta la sección "CONFIGURACIÓN" abajo (base_dir, lista de areas, nombres de archivos).
Si tu app que contiene el modelo Area tiene un nombre distinto, modifica el intento
de importación en la sección IMPORT (ver comentario).
"""
import os
from django.core.files import File
from django.db import IntegrityError, transaction

from area.models import Area

# ---------------------- CONFIGURACIÓN ----------------------
# Ruta donde están las imágenes de ejemplo (opcional)
base_dir = "/app/fixtures/areas"  # cambia a la ruta donde tengas las imágenes

# Lista de áreas a crear (nombre_area). Cambia, añade o quita según necesites.
areas = [
    {"nombre_area": "Matemáticas", "estado_area": True, "imagen": "matematicas.png"},
    {"nombre_area": "Lenguaje", "estado_area": True, "imagen": "lenguaje.png"},
    {"nombre_area": "Química", "estado_area": True, "imagen": "quimica.png"},
    {"nombre_area": "Inglés", "estado_area": True, "imagen": "ingles.png"},
    {"nombre_area": "Física", "estado_area": True, "imagen": "fisica.png"},
    {"nombre_area": "Música", "estado_area": True, "imagen": "musica.png"},
    {"nombre_area": "Nivelacion Academica Semillero", "estado_area": True, "imagen": "nas.png"},
    {"nombre_area": "Artes Escénicas", "estado_area": True, "imagen": "artes.png"},
    # Puedes añadir más entradas aquí. Si no quieres imagen, pon "imagen": None o elimina la clave.
]

# Si prefieres crear desde un CSV, cambia la lógica en main() para leer el archivo y poblar `areas`.
# -----------------------------------------------------------

def ensure_file(path):
    """Comprueba si existe el archivo y devuelve True/False."""
    if not path:
        return False
    if not os.path.exists(path):
        print(f"AVISO: archivo no encontrado: {path}. Se omitirá la imagen para este registro.")
        return False
    return True

def main():
    created = 0
    updated = 0
    for idx, item in enumerate(areas, start=1):
        nombre = item.get("nombre_area")
        estado = item.get("estado_area", True)
        imagen_nombre = item.get("imagen")  # nombre de archivo relativo a base_dir
        imagen_path = os.path.join(base_dir, imagen_nombre) if imagen_nombre else None

        try:
            with transaction.atomic():
                # Intentar obtener o crear (respeta unique=True en nombre_area)
                area_obj, was_created = Area.objects.get_or_create(
                    nombre_area=nombre,
                    defaults={"estado_area": estado}
                )

                # Si no fue creado, actualizar estado si es distinto
                if not was_created:
                    changed = False
                    if area_obj.estado_area != estado:
                        area_obj.estado_area = estado
                        changed = True
                    if changed:
                        area_obj.save()
                        updated += 1

                # Adjuntar imagen si existe y (a) el registro no tiene imagen o (b) quieres forzar reemplazo
                # Aquí solo añadimos la imagen si el archivo existe y el campo está vacío.
                if ensure_file(imagen_path):
                    # Si deseas forzar reemplazo incluso si ya tiene imagen, cambia la condición.
                    if not getattr(area_obj, "imagen_area", None):
                        with open(imagen_path, "rb") as f:
                            filename = f"{area_obj.pk}_{os.path.basename(imagen_nombre)}"
                            area_obj.imagen_area.save(filename, File(f), save=True)
                    else:
                        # ya tiene imagen: no hacemos nada; si quieres reemplazarla, descomenta/ajusta:
                        # with open(imagen_path, "rb") as f:
                        #     filename = f"{area_obj.pk}_{os.path.basename(imagen_nombre)}"
                        #     area_obj.imagen_area.save(filename, File(f), save=True)
                        pass

                if was_created:
                    created += 1
                    print(f"{idx}: Area creada: '{nombre}' (pk={area_obj.pk})")
                else:
                    print(f"{idx}: Area existente: '{nombre}' (pk={area_obj.pk})")

        except IntegrityError as e:
            print(f"ERROR de integridad creando/actualizando '{nombre}': {e}")
        except Exception as e:
            print(f"ERROR creando/actualizando '{nombre}': {e}")

    print(f"Fin: {created} creadas, {updated} actualizadas ({len(areas)} procesadas).")

if __name__ == "__main__":
    main()