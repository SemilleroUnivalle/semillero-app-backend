import pytest
from datetime import date
from oferta_categoria.serializers import OfertaCategoriaReadSerializer, OfertaCategoriaInscripcionReadSerializer, OfertaCategoriaWriteSerializer
from oferta_categoria.models import OfertaCategoria

@pytest.mark.django_db
def test_serializador_oferta_categoria_lectura(oferta_categoria_instance, modulo_instance):
    oferta_categoria_instance.modulo.add(modulo_instance)
    serializer = OfertaCategoriaReadSerializer(instance=oferta_categoria_instance)
    assert serializer.data['id_oferta_academica']['nombre'] == 'Semestre 2026-I'
    assert serializer.data['id_categoria']['nombre'] == 'Semillero Basico'
    assert len(serializer.data['modulo']) == 1
    assert serializer.data['modulo'][0]['nombre_modulo'] == 'Modulo Introductorio'

@pytest.mark.django_db
def test_serializador_oferta_categoria_escritura_crear_y_actualizar(oferta_academica_instance, categoria_instance, modulo_instance):
    data = {
        'id_oferta_academica': oferta_academica_instance.id_oferta_academica,
        'id_categoria': categoria_instance.id_categoria,
        'precio_publico': 70000.00,
        'precio_privado': 85000.00,
        'fecha_finalizacion': date(2026, 7, 31),
        'estado': True,
        'modulo': [modulo_instance.id_modulo]
    }
    serializer = OfertaCategoriaWriteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    oferta_cat = serializer.save()
    assert oferta_cat.id_oferta_categoria is not None
    assert oferta_cat.modulo.count() == 1

    # Probar actualización
    update_data = {
        'precio_publico': 75000.00,
        'modulo': []  # Eliminar todos los módulos
    }
    serializer_update = OfertaCategoriaWriteSerializer(instance=oferta_cat, data=update_data, partial=True)
    assert serializer_update.is_valid(), serializer_update.errors
    updated_instance = serializer_update.save()
    assert updated_instance.precio_publico == 75000.00
    assert updated_instance.modulo.count() == 0
