#!/usr/bin/env python3
"""
Script para crear inscripciones usando estudiantes id 1..20 y módulos id 1..20,
con asignación de módulos de forma aleatoria.

Uso:
    Desde la raíz del proyecto Django:
        python manage.py shell < crear_inscripciones.py

Ajustes en CONFIGURACIÓN abajo:
- BASE_DIR: carpeta donde poner archivos de ejemplo (recibo.pdf, certificado.pdf)
- CREATE_GROUP_ZERO: si True, el script intentará crear un Grupo con pk=0 si no existe.
- UNIQUE_MODULO_ASSIGNMENT: si True, cada estudiante recibirá un módulo distinto (si hay suficientes módulos).
  Si no hay suficientes módulos para asignación única, automáticamente se hace sampling con reemplazo.
- Si tus modelos están en apps con nombres distintos, ajusta los imports.
"""
import os
import random
from django.core.files import File
from django.db import transaction, IntegrityError

# ------------------ IMPORTS MODELOS (ajusta si tu proyecto usa otros paths) ------------------
from estudiante.models import Estudiante
from modulo.models import Modulo
from grupo.models import Grupo
from inscripcion.models import Inscripcion

# ---------------------------------------------------------------------------------------------

# ----------------------------- CONFIGURACIÓN ------------------------------------------------
BASE_DIR = "/app/fixtures/inscripciones"  # ruta donde colocar archivos de ejemplo (recibo.pdf, certificado.pdf)
RECURSOS = {
    "recibo_pago": "recibo_pago.pdf",
    "certificado": "certificado.pdf",
}
# Si quieres que el script cree un Grupo con pk=0 en caso de no existir, pon True.
CREATE_GROUP_ZERO = False

# Rango de ids a usar (estudiantes y módulos)
ESTUDIANTE_START = 1
ESTUDIANTE_END = 20
MODULO_START = 1
MODULO_END = 20

# Si True, intentamos asignar módulos únicos (sin repeticiones) cuando sea posible.
# Si no hay suficientes módulos, el script hará sampling con reemplazo para completar.
UNIQUE_MODULO_ASSIGNMENT = False

# Valores aleatorios posibles
TIPOS_VINCULACION = ["Regular", "Cultural", "Extraescolar", "Semillero"]
OBSERVACIONES_EJEMPLO = [
    "Inscripción sin observaciones.",
    "Requiere autorización de acudiente.",
    "Pago pendiente de conciliación.",
    "Estudiante con necesidades especiales (soporte requerido).",
    "Inscripción realizada vía convocatoria."
]
# ---------------------------------------------------------------------------------------------

def ensure_file(path):
    """Comprueba si existe el archivo y devuelve True/False."""
    if not path:
        return False
    if not os.path.exists(path):
        return False
    return True

def obtener_grupo_cero():
    """Intentar obtener Grupo con pk=0; si no existe y CREATE_GROUP_ZERO True, crear uno."""
    if Grupo is None:
        return None
    try:
        g = Grupo.objects.get(pk=0)
        print("Grupo con pk=0 encontrado.")
        return g
    except Grupo.DoesNotExist:
        if CREATE_GROUP_ZERO:
            try:
                # Intentamos crear con pk=0; si falla, capturamos la excepción y devolvemos None
                g = Grupo.objects.create(pk=0, nombre="Grupo 0")
                print("Grupo con pk=0 creado automáticamente.")
                return g
            except Exception as e:
                print(f"ERROR al crear Grupo pk=0: {e}. Se usará None para grupo.")
                return None
        else:
            print("No existe Grupo con pk=0 y CREATE_GROUP_ZERO=False. Se usará grupo=None para las inscripciones.")
            return None

def main():
    created = 0
    errors = 0

    # Preparar paths completos a archivos (si existen)
    recibo_path = os.path.join(BASE_DIR, RECURSOS["recibo_pago"]) if RECURSOS.get("recibo_pago") else None
    certificado_path = os.path.join(BASE_DIR, RECURSOS["certificado"]) if RECURSOS.get("certificado") else None

    grupo_instancia = obtener_grupo_cero()

    # Construir listas de ids
    estudiantes_ids = list(range(ESTUDIANTE_START, ESTUDIANTE_END + 1))
    modulos_ids = list(range(MODULO_START, MODULO_END + 1))

    if not estudiantes_ids:
        print("No hay estudiantes en el rango configurado. Abortando.")
        return

    if not modulos_ids:
        print("No hay módulos en el rango configurado. Abortando.")
        return

    # Preparar asignación aleatoria de módulos:
    # - Si UNIQUE_MODULO_ASSIGNMENT True y hay suficientes módulos, usamos random.sample para asignar sin repeticiones.
    # - Si no hay suficientes módulos o UNIQUE_MODULO_ASSIGNMENT False, permitimos repeticiones (random.choices o random.choice).
    num_estudiantes = len(estudiantes_ids)
    asignacion_modulos = []

    if UNIQUE_MODULO_ASSIGNMENT:
        if len(modulos_ids) >= num_estudiantes:
            asignacion_modulos = random.sample(modulos_ids, k=num_estudiantes)
            print("Asignación aleatoria única de módulos (sin repeticiones) creada.")
        else:
            # No hay suficientes módulos para asignación única; fallback a sampling con reemplazo
            asignacion_modulos = random.choices(modulos_ids, k=num_estudiantes)
            print("AVISO: No hay suficientes módulos para asignación única. Se hará sampling con reemplazo (podrán repetirse módulos).")
    else:
        # Permitir repeticiones
        asignacion_modulos = [random.choice(modulos_ids) for _ in range(num_estudiantes)]
        print("Asignación aleatoria de módulos (con posibles repeticiones) creada.")

    # Ahora iteramos por cada estudiante y su módulo asignado
    for est_id, mod_id in zip(estudiantes_ids, asignacion_modulos):
        try:
            estudiante = Estudiante.objects.get(pk=est_id)
        except Estudiante.DoesNotExist:
            print(f"SKIP: Estudiante con pk={est_id} no encontrado.")
            errors += 1
            continue

        try:
            modulo = Modulo.objects.get(pk=mod_id)
        except Modulo.DoesNotExist:
            print(f"SKIP: Modulo con pk={mod_id} no encontrado (asignado a estudiante {est_id}).")
            errors += 1
            continue

        tipo_vinc = random.choice(TIPOS_VINCULACION)
        observ = random.choice(OBSERVACIONES_EJEMPLO)
        terminos = True  # por defecto

        try:
            with transaction.atomic():
                ins = Inscripcion.objects.create(
                    id_estudiante=estudiante,
                    id_modulo=modulo,
                    grupo=grupo_instancia,  # puede ser None si no existe pk=0
                    tipo_vinculacion=tipo_vinc,
                    terminos=terminos,
                    observaciones=observ
                )

                # Adjuntar archivos si existen (usar save=False y luego save())
                if ensure_file(recibo_path):
                    with open(recibo_path, "rb") as f:
                        ins.recibo_pago.save(f"{ins.pk}_recibo.pdf", File(f), save=False)

                if ensure_file(certificado_path):
                    with open(certificado_path, "rb") as f:
                        ins.certificado.save(f"{ins.pk}_certificado.pdf", File(f), save=False)

                # Guardar cambios (archivos)
                ins.save()

                created += 1
                print(f"{created}: Inscripcion creada -> estudiante_id={est_id}, modulo_id={mod_id}, pk_inscripcion={ins.pk}")
        except IntegrityError as e:
            print(f"ERROR de integridad creando inscripcion (est={est_id}, mod={mod_id}): {e}")
            errors += 1
        except Exception as e:
            print(f"ERROR creando inscripcion (est={est_id}, mod={mod_id}): {e}")
            errors += 1

    print(f"Finalizado: {created} inscripciones creadas, {errors} errores/skips.")

if __name__ == "__main__":
    main()