from rest_framework import serializers
from .models import Modulo
from categoria.models import Categoria
from oferta_categoria.serializers import OfertaCategoriaReadSerializer

# Serializador para las categorías
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        ref_name = 'CategoriaSerializerEnModulo'

# Serializador para lecturas (GET) - con depth=1 para mostrar relaciones anidadas
class ModuloReadSerializer(serializers.ModelSerializer):
    # Incluimos la categoría relacionada (ahora como objeto único)
    id_categoria = CategoriaSerializer(read_only=True)
    #id_oferta_categoria = OfertaCategoriaReadSerializer (many=True, read_only=True)

    class Meta:
        model = Modulo
        fields = '__all__'
#Serializador para mostrar el modulo que tiene el profesor osea que excluimos la información de la categoria
class ModuloProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = '__all__'

# Serializador para escrituras (POST/PUT/PATCH) - sin depth
class ModuloWriteSerializer(serializers.ModelSerializer):
    # Campo para asociar una única categoría (ForeignKey)
    id_categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        required=False
    )
    
    class Meta:
        model = Modulo
        fields = '__all__'
    
    def create(self, validated_data):
        return Modulo.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Actualizar todos los campos, incluida la categoría
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

