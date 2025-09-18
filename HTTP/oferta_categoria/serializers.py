from rest_framework import serializers
from .models import OfertaCategoria
from modulo.models import Modulo
from oferta_academica.serializers import OfertaAcademicaSerializer

# Serializador para los módulos
class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = '__all__'
        ref_name = 'ModuloSerializerEnOfertaCategoria'  # Añadido para evitar conflictos de referencia

# Serializador para lecturas (GET) - con depth=1 para mostrar relaciones anidadas
class OfertaCategoriaReadSerializer(serializers.ModelSerializer):
    #modulo = ModuloSerializer(many=True, read_only=True)
    id_oferta_academica = OfertaAcademicaSerializer(read_only=True)

    class Meta:
        model = OfertaCategoria
        fields = '__all__'
        
class OfertaCategoriaInscripcionReadSerializer(serializers.ModelSerializer):
    id_oferta_academica = OfertaAcademicaSerializer(read_only=True)

    class Meta:
        model = OfertaCategoria
        fields = '__all__'

# Serializador para escrituras (POST/PUT/PATCH) - sin depth
class OfertaCategoriaWriteSerializer(serializers.ModelSerializer):
    # Usamos PrimaryKeyRelatedField para aceptar una lista de IDs de módulos
    modulo = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Modulo.objects.all() 
    )

    class Meta:
        model = OfertaCategoria
        fields = '__all__'

    def create(self, validated_data):
        modulos = validated_data.pop('modulo', []) 
        oferta_categoria = OfertaCategoria.objects.create(**validated_data)
        oferta_categoria.modulo.set(modulos)
        return oferta_categoria

    def update(self, instance, validated_data):
        modulos = validated_data.pop('modulo', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.modulo.set(modulos) 
        
        return instance