import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semillero_backend.settings')
django.setup()

from inscripcion.models import Inscripcion

def sync_estados():
    inscripciones = Inscripcion.objects.all()
    count_updated = 0
    
    print(f"Starting state recalculation for {inscripciones.count()} inscriptions...")
    for ins in inscripciones:
        recibo_pago_nuevo = ins.verificacion_recibo_pago
        constancia_nuevo = ins.verificacion_constancia
        certificado_nuevo = ins.verificacion_certificado
        recibo_servicio_nuevo = ins.verificacion_recibo_servicio
        
        has_uploaded_files = bool(
            ins.recibo_pago or
            ins.constancia or
            ins.certificado or
            ins.recibo_servicio
        )
        
        estudiante_verificado = ins.id_estudiante.verificacion_informacion if ins.id_estudiante else False
        
        old_estado = ins.estado
        
        if has_uploaded_files:
            documentos_verificados = []
            if ins.recibo_pago:
                documentos_verificados.append(recibo_pago_nuevo)
            if ins.constancia:
                documentos_verificados.append(constancia_nuevo)
            if ins.certificado:
                documentos_verificados.append(certificado_nuevo)
            if ins.recibo_servicio:
                documentos_verificados.append(recibo_servicio_nuevo)
                
            if all(documentos_verificados) and estudiante_verificado:
                ins.estado = "Revisado"
            elif any(documentos_verificados) or estudiante_verificado:
                ins.estado = "Pendiente"
            else:
                ins.estado = "No revisado"
        else:
            verificaciones_manuales = [recibo_pago_nuevo, certificado_nuevo, recibo_servicio_nuevo]
            if any(verificaciones_manuales):
                if estudiante_verificado:
                    ins.estado = "Revisado"
                else:
                    ins.estado = "Pendiente"
            else:
                ins.estado = "No revisado"
                
        if old_estado != ins.estado:
            ins.save(update_fields=['estado'])
            count_updated += 1
            print(f"ID {ins.id_inscripcion} ({ins.id_modulo.nombre_modulo if ins.id_modulo else 'No modulo'}): {old_estado} -> {ins.estado}")
            
    print(f"Finished. Recalculated states. {count_updated} registrations updated.")

if __name__ == "__main__":
    sync_estados()
