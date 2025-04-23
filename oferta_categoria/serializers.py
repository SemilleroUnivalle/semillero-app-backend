from rest_framework import serializers
from .models import OfertaCategoria

# Serializador para lecturas (GET) - con depth=1 para mostrar relaciones anidadas
class OfertaCategoriaReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaCategoria
        fields = '__all__'
        depth = 1  # Mantiene la profundidad para mostrar datos relacionados

# Serializador para escrituras (POST/PUT/PATCH) - sin depth
class OfertaCategoriaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaCategoria
        fields = '__all__'
        # No usamos depth aquí