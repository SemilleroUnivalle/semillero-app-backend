import random
from decimal import Decimal
from django.db import transaction
from profesor.models import Profesor
from inscripcion.models import Inscripcion
from seguimiento_academico.models import SeguimientoAcademico

def main():
    print("Iniciando llenado de notas para el dashboard (Profesor 400)...")
    
    try:
        # 1. Buscar al profesor 400
        profesor = Profesor.objects.get(numero_documento="400")
        print(f"Profesor encontrado: {profesor.nombre} {profesor.apellido}")
        
        # 2. Obtener todas las inscripciones en sus grupos
        inscripciones = Inscripcion.objects.filter(grupo__profesor=profesor)
        print(f"Estudiantes a calificar: {inscripciones.count()}")
        
        if not inscripciones.exists():
            print("AVISO: El profesor 400 no tiene estudiantes asignados en grupos.")
            return

        notas_creadas = 0
        notas_actualizadas = 0

        with transaction.atomic():
            for insc in inscripciones:
                # Generar notas aleatoriamente para simular datos reales de dashboard
                # Usamos un rango de 3.0 a 5.0 para que se vea "bien" en el dashboard
                s1 = Decimal(random.uniform(3.0, 5.0)).quantize(Decimal('0.00'))
                s2 = Decimal(random.uniform(2.5, 5.0)).quantize(Decimal('0.00'))
                nd = Decimal(random.uniform(3.5, 5.0)).quantize(Decimal('0.00'))
                ne = Decimal(random.uniform(3.5, 5.0)).quantize(Decimal('0.00'))
                
                # Buscar o crear el seguimiento
                seguimiento, created = SeguimientoAcademico.objects.get_or_create(
                    id_inscripcion=insc,
                    defaults={
                        'seguimiento_1': s1,
                        'seguimiento_2': s2,
                        'nota_conceptual_docente': nd,
                        'nota_conceptual_estudiante': ne,
                        'observaciones': "Nota generada para pruebas de dashboard"
                    }
                )
                
                if not created:
                    # Si ya existía, actualizamos los valores
                    seguimiento.seguimiento_1 = s1
                    seguimiento.seguimiento_2 = s2
                    seguimiento.nota_conceptual_docente = nd
                    seguimiento.nota_conceptual_estudiante = ne
                    seguimiento.save()
                    notas_actualizadas += 1
                else:
                    notas_creadas += 1

        print(f"\nProceso finalizado con éxito:")
        print(f"✓ Registros nuevos creados: {notas_creadas}")
        print(f"✓ Registros actualizados: {notas_actualizadas}")
        print(f"Total estudiantes calificados: {notas_creadas + notas_actualizadas}")

    except Profesor.DoesNotExist:
        print("ERROR: No se encontró al profesor con número de documento 400.")
    except Exception as e:
        print(f"ERROR inesperado: {e}")

if __name__ == "__main__":
    main()
