from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import date
from oferta_academica.models import OfertaAcademica
from categoria.models import Categoria
from oferta_categoria.models import OfertaCategoria

class OfertaCategoriaEndpointTests(APITestCase):
    def setUp(self):
        # Crear categoría de prueba
        self.categoria = Categoria.objects.create(
            nombre="Categoria Prueba",
            estado=True
        )
        
        # Crear ofertas académicas
        self.oferta_activa = OfertaAcademica.objects.create(
            nombre="Oferta Activa",
            fecha_inicio=date.today(),
            estado="inscripcion"
        )
        self.oferta_inactiva = OfertaAcademica.objects.create(
            nombre="Oferta Inactiva",
            fecha_inicio=date.today(),
            estado="finalizado"
        )

        # Crear ofertas categorías
        self.oferta_categoria_activa = OfertaCategoria.objects.create(
            id_oferta_academica=self.oferta_activa,
            id_categoria=self.categoria,
            precio_publico=100000.00,
            precio_privado=120000.00,
            fecha_finalizacion=date.today(),
            estado=True
        )
        self.oferta_categoria_inactiva = OfertaCategoria.objects.create(
            id_oferta_academica=self.oferta_inactiva,
            id_categoria=self.categoria,
            precio_publico=100000.00,
            precio_privado=120000.00,
            fecha_finalizacion=date.today(),
            estado=True
        )

    def test_obtener_oferta_categoria_por_oferta_academica(self):
        url = reverse('OfertaCategoria-obtener-oferta-categoria-por-oferta-academica')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Debe contener la oferta activa pero no la inactiva
        data = response.json()
        active_key = str(self.oferta_activa.id_oferta_academica)
        inactive_key = str(self.oferta_inactiva.id_oferta_academica)
        
        self.assertIn(active_key, data)
        self.assertNotIn(inactive_key, data)
        
        # Verificar que el elemento devuelto tiene los datos correctos
        items = data[active_key]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['id_oferta_categoria'], self.oferta_categoria_activa.id_oferta_categoria)
