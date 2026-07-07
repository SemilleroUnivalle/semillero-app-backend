import pytest
from decimal import Decimal
from prueba_diagnostica.models import PruebaDiagnostica, PreguntaDiagnostica, RespuestaDiagnostica
from prueba_diagnostica.serializers import (
    RespuestaDiagnosticaSerializer, RespuestaDiagnosticaWriteSerializer,
    PreguntaDiagnosticaReadSerializer, PreguntaDiagnosticaWriteSerializer,
    PruebaDiagnosticaReadSerializer, PruebaDiagnosticaWriteSerializer,
    PreguntaConRespuestasSerializer
)

@pytest.fixture
def instancia_prueba_diagnostica(db, modulo_instance):
    return PruebaDiagnostica.objects.create(
        id_modulo=modulo_instance,
        nombre_prueba='Prueba de Matematicas',
        descripcion='Prueba inicial de algebra',
        tiempo_limite=45,
        puntaje_minimo=60.00
    )

@pytest.mark.django_db
def test_serializador_escritura_prueba_diagnostica_valido(modulo_instance):
    data = {
        'id_modulo': modulo_instance.id_modulo,
        'nombre_prueba': 'Prueba Fisica',
        'descripcion': 'Mecanica',
        'tiempo_limite': 30,
        'puntaje_minimo': 70.00,
        'estado': True
    }
    serializer = PruebaDiagnosticaWriteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    prueba = serializer.save()
    assert prueba.id_prueba is not None
    assert prueba.nombre_prueba == 'Prueba Fisica'

@pytest.mark.django_db
def test_serializador_pregunta_con_respuestas_crear(instancia_prueba_diagnostica):
    data = {
        'id_prueba': instancia_prueba_diagnostica.id_prueba,
        'texto_pregunta': '¿Cuánto es 2 + 2?',
        'tipo_pregunta': 'multiple',
        'puntaje': 5.00,
        'estado': True,
        'respuestas': [
            {'texto_respuesta': '3', 'es_correcta': False},
            {'texto_respuesta': '4', 'es_correcta': True}
        ]
    }
    serializer = PreguntaConRespuestasSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    pregunta = serializer.save()
    assert pregunta.id_pregunta is not None
    assert pregunta.respuestas.count() == 2
    assert pregunta.respuestas.filter(es_correcta=True).first().texto_respuesta == '4'

@pytest.mark.django_db
def test_serializador_pregunta_con_respuestas_actualizar(instancia_prueba_diagnostica):
    pregunta = PreguntaDiagnostica.objects.create(
        id_prueba=instancia_prueba_diagnostica,
        texto_pregunta='¿Cuánto es 1 + 1?',
        tipo_pregunta='multiple',
        puntaje=2.00
    )
    RespuestaDiagnostica.objects.create(id_pregunta=pregunta, texto_respuesta='2', es_correcta=True)
    
    update_data = {
        'texto_pregunta': '¿Cuánto es 1 + 1 actualizado?',
        'respuestas': [
            {'texto_respuesta': '3', 'es_correcta': False},
            {'texto_respuesta': '2', 'es_correcta': True}
        ]
    }
    serializer = PreguntaConRespuestasSerializer(instance=pregunta, data=update_data, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated_pregunta = serializer.save()
    assert updated_pregunta.texto_pregunta == '¿Cuánto es 1 + 1 actualizado?'
    # Las respuestas deberían haber sido reemplazadas
    assert updated_pregunta.respuestas.count() == 2
