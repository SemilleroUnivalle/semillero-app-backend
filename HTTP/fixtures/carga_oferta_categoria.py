#!/usr/bin/env python3
"""
Script para crear/actualizar Oferta Categoría y asociar módulos.

Uso:
    Desde la raíz del proyecto Django:
        python manage.py shell -c "exec(open('fixtures/carga_oferta_categoria.py').read()); main()"
"""
from django.db import IntegrityError, transaction
from datetime import date

from oferta_categoria.models import OfertaCategoria
from oferta_academica.models import OfertaAcademica
from categoria.models import Categoria
from modulo.models import Modulo

# ---------------------- CONFIGURACIÓN ----------------------
# Rango de módulos a asociar
MODULO_START = 1
MODULO_END = 20

# Datos de la oferta categoría
OFERTA_CATEGORIA_DATA = {
    "precio_publico": 1000,
    "precio_privado": 1000,
    "precio_univalle": 1000,
    "precio_univalle_egresados": 800,  # Opcional
    "fecha_finalizacion": date(2025, 4, 25),
    "estado": True,
    "nombre_oferta_academica": "2025",  # Nombre de la oferta académica a buscar
    "id_categoria": 1  # ID de la categoría
}
# -----------------------------------------------------------

def main():
    created = 0
    updated = 0
    
    # Obtener la oferta académica
    try:
        oferta_academica = OfertaAcademica.objects.get(nombre=OFERTA_CATEGORIA_DATA["nombre_oferta_academica"])
        print(f"Oferta Académica encontrada: {oferta_academica.nombre} (pk={oferta_academica.pk})")
    except OfertaAcademica.DoesNotExist:
        print(f"ERROR: No se encontró la Oferta Académica con nombre '{OFERTA_CATEGORIA_DATA['nombre_oferta_academica']}'")
        print("Asegúrate de ejecutar primero carga_oferta_academica.py")
        return
    
    # Obtener la categoría
    try:
        categoria = Categoria.objects.get(pk=OFERTA_CATEGORIA_DATA["id_categoria"])
        print(f"Categoría encontrada: {categoria.nombre} (pk={categoria.pk})")
    except Categoria.DoesNotExist:
        print(f"ERROR: No se encontró la Categoría con pk={OFERTA_CATEGORIA_DATA['id_categoria']}")
        return
    
    try:
        with transaction.atomic():
            # Intentar obtener o crear la oferta categoría
            oferta_cat_obj, was_created = OfertaCategoria.objects.get_or_create(
                id_oferta_academica=oferta_academica,
                id_categoria=categoria,
                defaults={
                    "precio_publico": OFERTA_CATEGORIA_DATA["precio_publico"],
                    "precio_privado": OFERTA_CATEGORIA_DATA["precio_privado"],
                    "precio_univalle": OFERTA_CATEGORIA_DATA["precio_univalle"],
                    "precio_univalle_egresados": OFERTA_CATEGORIA_DATA.get("precio_univalle_egresados"),
                    "fecha_finalizacion": OFERTA_CATEGORIA_DATA["fecha_finalizacion"],
                    "estado": OFERTA_CATEGORIA_DATA["estado"]
                }
            )

            # Si no fue creado, actualizar si es necesario
            if not was_created:
                changed = False
                if oferta_cat_obj.precio_publico != OFERTA_CATEGORIA_DATA["precio_publico"]:
                    oferta_cat_obj.precio_publico = OFERTA_CATEGORIA_DATA["precio_publico"]
                    changed = True
                if oferta_cat_obj.precio_privado != OFERTA_CATEGORIA_DATA["precio_privado"]:
                    oferta_cat_obj.precio_privado = OFERTA_CATEGORIA_DATA["precio_privado"]
                    changed = True
                if oferta_cat_obj.precio_univalle != OFERTA_CATEGORIA_DATA["precio_univalle"]:
                    oferta_cat_obj.precio_univalle = OFERTA_CATEGORIA_DATA["precio_univalle"]
                    changed = True
                if oferta_cat_obj.fecha_finalizacion != OFERTA_CATEGORIA_DATA["fecha_finalizacion"]:
                    oferta_cat_obj.fecha_finalizacion = OFERTA_CATEGORIA_DATA["fecha_finalizacion"]
                    changed = True
                if oferta_cat_obj.estado != OFERTA_CATEGORIA_DATA["estado"]:
                    oferta_cat_obj.estado = OFERTA_CATEGORIA_DATA["estado"]
                    changed = True
                if changed:
                    oferta_cat_obj.save()
                    updated += 1

            if was_created:
                created += 1
                print(f"Oferta Categoría creada (pk={oferta_cat_obj.pk})")
            else:
                print(f"Oferta Categoría existente (pk={oferta_cat_obj.pk})")
            
            # Asociar módulos (del 1 al 20)
            modulos_asociados = 0
            modulos_no_encontrados = 0
            
            for modulo_id in range(MODULO_START, MODULO_END + 1):
                try:
                    modulo = Modulo.objects.get(pk=modulo_id)
                    # Agregar la oferta categoría al módulo (ManyToMany)
                    modulo.id_oferta_categoria.add(oferta_cat_obj)
                    modulos_asociados += 1
                    print(f"  - Módulo {modulo_id} ({modulo.nombre_modulo}) asociado")
                except Modulo.DoesNotExist:
                    print(f"  - AVISO: Módulo con pk={modulo_id} no encontrado")
                    modulos_no_encontrados += 1
            
            print(f"\nMódulos asociados: {modulos_asociados}/{MODULO_END - MODULO_START + 1}")
            if modulos_no_encontrados > 0:
                print(f"Módulos no encontrados: {modulos_no_encontrados}")

    except IntegrityError as e:
        print(f"ERROR de integridad creando/actualizando Oferta Categoría: {e}")
    except Exception as e:
        print(f"ERROR creando/actualizando Oferta Categoría: {e}")

    print(f"\nFin: {created} ofertas categoría creadas, {updated} actualizadas.")

if __name__ == "__main__":
    main()
