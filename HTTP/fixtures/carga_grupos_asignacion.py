import os
import random
from django.db import transaction
from profesor.models import Profesor
from monitor_academico.models import MonitorAcademico
from estudiante.models import Estudiante
from grupo.models import Grupo
from inscripcion.models import Inscripcion

def main():
    print("Iniciando asignación de grupos...")
    
    # 1. Obtener profesores y monitores disponibles
    profesores = list(Profesor.objects.all())
    monitores = list(MonitorAcademico.objects.all())
    
    if not profesores:
        print("ERROR: No hay profesores cargados.")
        return

    # 2. Obtener inscripciones que no tienen grupo asignado
    inscripciones_pendientes = list(Inscripcion.objects.filter(grupo__isnull=True))
    
    if not inscripciones_pendientes:
        print("AVISO: No hay inscripciones pendientes de grupo (o todas ya tienen uno).")
        # Vamos a tomar algunas existentes para el ejemplo si es necesario
        inscripciones_pendientes = list(Inscripcion.objects.all())[:50]

    if not inscripciones_pendientes:
        print("ERROR: No hay inscripciones en el sistema.")
        return

    # 3. Crear grupos y asignar
    num_grupos = 5
    estudiantes_por_grupo = 5
    
    for i in range(num_grupos):
        try:
            with transaction.atomic():
                profesor = profesores[i % len(profesores)]
                monitor = monitores[i % len(monitores)] if monitores else None
                
                # Cambiado de letras (chr(65+i)) a números (i+1)
                nombre_grupo = f"Grupo {i+1} - {profesor.nombre}"
                
                # Crear el grupo con el profesor ya asignado
                grupo, created = Grupo.objects.get_or_create(
                    nombre=nombre_grupo,
                    defaults={'profesor': profesor, 'monitor_academico': monitor}
                )
                
                if not created:
                    # Si ya existía, nos aseguramos que el profesor sea el correcto
                    grupo.profesor = profesor
                    grupo.monitor_academico = monitor
                    grupo.save()

                # Tomar un bloque de inscripciones
                inicio = i * estudiantes_por_grupo
                fin = inicio + estudiantes_por_grupo
                bloque_inscripciones = inscripciones_pendientes[inicio:fin]
                
                # Asignar el grupo a las inscripciones
                for inscripcion in bloque_inscripciones:
                    inscripcion.grupo = grupo
                    inscripcion.save()
                
                print(f"✓ Creado '{nombre_grupo}' con {len(bloque_inscripciones)} estudiantes.")
                print(f"  Profesor: {profesor.nombre} {profesor.apellido} | ID/Documento: {profesor.numero_documento}")
                print("-" * 50)
                
        except Exception as e:
            print(f"Error procesando grupo {i}: {e}")

    print("\nFin de la asignación.")

if __name__ == "__main__":
    main()
