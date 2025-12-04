#!/usr/bin/env python3
"""
Script para crear/actualizar Modulo según la estructura proporcionada,
adjuntando la imagen correspondiente por área desde base_dir.

Uso:
    Desde la raíz del proyecto Django:
        python manage.py shell < crear_modulos.py

Notas:
- Ajusta los imports si tus apps tienen nombres distintos.
- base_dir debe existir y contener las imágenes:
    /app/fixtures/modulos/matematicas.png
    /app/fixtures/modulos/lenguaje.png
    /app/fixtures/modulos/quimica.png
    /app/fixtures/modulos/ingles.png
    /app/fixtures/modulos/fisica.png
    /app/fixtures/modulos/musica.png
    /app/fixtures/modulos/nas.png
    /app/fixtures/modulos/artes.png
"""
import os
from django.core.files import File
from django.db import transaction, IntegrityError

from modulo.models import Modulo
from area.models import Area
from categoria.models import Categoria


# ---------------------- CONFIGURACIÓN ----------------------
base_dir = "/app/fixtures/modulos"  # donde están las imágenes

# Mapeo de imagen por id_area (según lo solicitado)
IMAGEN_POR_AREA = {
    1: "matematicas.png",
    2: "lenguaje.png",
    3: "quimica.png",
    4: "ingles.png",
    5: "fisica.png",
    6: "musica.png",
    7: "nas.png",
    8: "artes.png",
}

# Estructura de módulos por área/categoría
modules_data = [
    # id_area 1, id_categoria 1
    {
        "id_area": 1, "id_categoria": 1,
        "modules": [
            {"dirigido_a": "6 a 7", "nombres": "De los enteros a los racionales"},
            {"dirigido_a": "7 a 11", "nombres": "Lógica y Conjuntos"},
            {"dirigido_a": "8 a 11", "nombres": "Sistemas Numéricos, Algebra Fundamental, Geometría Plana y del Espacio, Geometría Analítica, Trigonometría"},
        ]
    },
    # id_area 2, id_categoria 1
    {
        "id_area": 2, "id_categoria": 1,
        "modules": [
            {"dirigido_a": "8 a 11", "nombres": "Escritura Creativa"},
            {"dirigido_a": "10 a 11", "nombres": "Lectura Critica"},
        ]
    },
    # id_area 3, id_categoria 1
    {
        "id_area": 3, "id_categoria": 1,
        "modules": [
            {"dirigido_a": "10 a 11", "nombres": "AGE: Atomo, Gases y Estequiometria I"},
        ]
    },
    # id_area 4, id_categoria 1
    {
        "id_area": 4, "id_categoria": 1,
        "modules": [
            {"dirigido_a": "8 a 11", "nombres": "Ingles Basico I, Ingles Basico II"},
        ]
    },
    # id_area 5, id_categoria 1
    {
        "id_area": 5, "id_categoria": 1,
        "modules": [
            {"dirigido_a": "10 a 11", "nombres": "Energia y Movimiento"},
        ]
    },
    # id_area 6, id_categoria 1
    {
        "id_area": 6, "id_categoria": 1,
        "modules": [
            {"dirigido_a": "8 a 11", "nombres": "Musica, Percucion y Flauta Dulce"},
        ]
    },
    # id_area 7, id_categoria 2
    {
        "id_area": 7, "id_categoria": 2,
        "modules": [
            {"dirigido_a": "10 a 11 y Egresados", "nombres": "Nivelación Academica Semillero - Sabados, Nivelación Academica Semillero - Semana"},
        ]
    },
    # id_area 8, id_categoria 1
    {
        "id_area": 8, "id_categoria": 1,
        "modules": [
            {"dirigido_a": "1 a 5", "nombres": "Taller infantil de Teatro"},
            {"dirigido_a": "6 a 11", "nombres": "Taller Juvenil de Teatro"},
        ]
    },
]

# Intensidad horaria por categoria id
INTENSIDAD_POR_CATEGORIA = {
    1: 48,
    2: 124,
}
# -----------------------------------------------------------

def ensure_file(path):
    if not path:
        return False
    if not os.path.exists(path):
        print(f"AVISO: imagen no encontrada: {path} (se omitirá imagen).")
        return False
    return True

def get_area_instance(pk):
    if Area is None:
        return None
    try:
        return Area.objects.get(pk=pk)
    except Area.DoesNotExist:
        return None

def get_categoria_instance(pk):
    if Categoria is None:
        return None
    try:
        return Categoria.objects.get(pk=pk)
    except Categoria.DoesNotExist:
        return None

def main():
    created = 0
    updated = 0
    skipped = 0

    for entry in modules_data:
        id_area = entry.get("id_area")
        id_categoria = entry.get("id_categoria")
        area_obj = get_area_instance(id_area)
        cat_obj = get_categoria_instance(id_categoria)

        if area_obj is None:
            print(f"SKIP: Area id={id_area} no encontrada. Saltando sus módulos.")
            skipped += 1
            continue
        if cat_obj is None:
            print(f"SKIP: Categoria id={id_categoria} no encontrada. Saltando sus módulos.")
            skipped += 1
            continue

        intensidad = INTENSIDAD_POR_CATEGORIA.get(id_categoria, 0)
        imagen_nombre_area = IMAGEN_POR_AREA.get(id_area)

        for mod in entry.get("modules", []):
            dirigido_a = mod.get("dirigido_a", "")
            nombres_raw = mod.get("nombres", "")

            # Si hay múltiples nombres separados por comas, crear un módulo por cada uno
            nombres_list = [n.strip() for n in nombres_raw.split(",") if n.strip()]

            for nombre in nombres_list:
                try:
                    with transaction.atomic():
                        # get_or_create por nombre único
                        obj, was_created = Modulo.objects.get_or_create(
                            nombre_modulo=nombre,
                            defaults={
                                "id_area": area_obj,
                                "id_categoria": cat_obj,
                                "descripcion_modulo": "",
                                "intensidad_horaria": intensidad,
                                "dirigido_a": dirigido_a,
                                "incluye": "",
                                "estado": True,
                            }
                        )

                        # Si no fue creado, actualizar campos que correspondan (área, categoría, intensidad, dirigido_a)
                        if not was_created:
                            changed = False
                            if obj.id_area_id != area_obj.pk:
                                obj.id_area = area_obj
                                changed = True
                            if obj.id_categoria_id != cat_obj.pk:
                                obj.id_categoria = cat_obj
                                changed = True
                            if obj.intensidad_horaria != intensidad:
                                obj.intensidad_horaria = intensidad
                                changed = True
                            if (obj.dirigido_a or "") != dirigido_a:
                                obj.dirigido_a = dirigido_a
                                changed = True
                            if changed:
                                obj.save()
                                updated += 1

                        # Adjuntar imagen del área si existe
                        if imagen_nombre_area:
                            imagen_path = os.path.join(base_dir, imagen_nombre_area)
                            if ensure_file(imagen_path):
                                # Si ya existe una imagen y quieres no sobrescribirla, podrías comprobar obj.imagen_modulo
                                # Aquí se sobreescribe siempre para asegurar la imagen por área
                                with open(imagen_path, "rb") as f:
                                    filename = f"{obj.pk}_{os.path.basename(imagen_nombre_area)}"
                                    obj.imagen_modulo.save(filename, File(f), save=True)

                        if was_created:
                            created += 1
                            print(f"CREADO: '{nombre}' (area={id_area}, categoria={id_categoria}, pk={obj.pk})")
                        else:
                            print(f"EXISTENTE: '{nombre}' (pk={obj.pk}) - verificado/actualizado")
                except IntegrityError as e:
                    print(f"ERROR de integridad creando '{nombre}': {e}")
                except Exception as e:
                    print(f"ERROR creando/actualizando '{nombre}': {e}")

    print(f"Fin: {created} creados, {updated} actualizados, {skipped} entradas saltadas.")

if __name__ == "__main__":
    main()