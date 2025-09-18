from rest_framework import serializers
from .models import Inscripcion

from modulo.serializers import ModuloReadSerializer
from modulo.models import Modulo

from estudiante.serializers import EstudianteSerializer
from estudiante.models import Estudiante

from oferta_categoria.serializers import OfertaCategoriaInscripcionReadSerializer
from oferta_categoria.models import OfertaCategoria

class InscripcionSerializer(serializers.ModelSerializer):
    id_modulo = serializers.PrimaryKeyRelatedField(queryset=Modulo.objects.all(), write_only=True)
    modulo = ModuloReadSerializer(source='id_modulo', read_only=True)

    id_estudiante = serializers.PrimaryKeyRelatedField(queryset=Estudiante.objects.all(), write_only=True)
    estudiante = EstudianteSerializer(source='id_estudiante', read_only=True)

    id_oferta_categoria = serializers.PrimaryKeyRelatedField(queryset=OfertaCategoria.objects.all(), write_only=True)
    oferta_categoria = OfertaCategoriaInscripcionReadSerializer(source='id_oferta_categoria', read_only=True)

    class Meta:
        model = Inscripcion
        fields = '__all__'
        read_only_fields = ('id_inscripcion',)
        