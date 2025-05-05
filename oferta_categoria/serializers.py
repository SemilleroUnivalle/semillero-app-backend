from rest_framework import serializers
from .models import OfertaCategoria
from modulo.models import Modulo

# Serializador para los módulos
class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = '__all__'
        ref_name = 'ModuloSerializerEnOfertaCategoria'  # Añadido para evitar conflictos de referencia

# Serializador para lecturas (GET) - con depth=1 para mostrar relaciones anidadas
class OfertaCategoriaReadSerializer(serializers.ModelSerializer):
    # Incluimos los módulos relacionados
    modulo = ModuloSerializer(many=True, read_only=True)

    class Meta:
        model = OfertaCategoria
        fields = '__all__'
        depth = 1  

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
        # Extraemos los módulos enviados por el frontend
        modulos = validated_data.pop('modulo', []) 
        
        # Extraemos los IDs de los módulos
        modulos_ids = [mod.id_modulo for mod in modulos]  
        
        # Verificamos si alguno de los módulos ya está asignado
        modulos_asignados = Modulo.objects.filter(id_oferta_categoria__isnull=False, id_modulo__in=modulos_ids)
        if modulos_asignados.exists():
            modulos_asignados_nombres = ", ".join(modulo.nombre_modulo for modulo in modulos_asignados)
            raise serializers.ValidationError(
                f"Los siguientes módulos ya están asignados a otra oferta categoría: {modulos_asignados_nombres}."
            )
        
        #if not modulos:
        #    raise serializers.ValidationError("Se requiere al menos un módulo para crear la oferta categoría.")
        
        # Creamos la oferta categoría
        oferta_categoria = OfertaCategoria.objects.create(**validated_data)
        
        # Asociamos los módulos a la oferta creada
        oferta_categoria.modulo.set(modulos)  # Usamos `set()` para establecer la relación
        
        return oferta_categoria

    def update(self, instance, validated_data):
        # Extraemos los IDs de los módulos enviados por el frontend
        modulos = validated_data.pop('modulo', [])  # Correcto: usamos 'modulo'
        
        # Actualizamos los campos de la OfertaCategoria
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualizamos la relación con los módulos
        instance.modulo.set(modulos)  # Usamos `set()` para actualizar la relación
        
        return instance