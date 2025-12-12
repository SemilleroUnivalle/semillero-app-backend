"""
Script para cargar preguntas de ejemplo al banco de preguntas.
Estas preguntas no están asociadas a ninguna prueba y pueden ser reutilizadas.

Ejecutar desde: HTTP/
Comando: python -m fixtures.carga_banco_preguntas
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semillero.settings')
django.setup()

from prueba_diagnostica.models import PreguntaDiagnostica, RespuestaDiagnostica
from django.db import transaction


def crear_preguntas_banco():
    """Crea preguntas de ejemplo en el banco."""
    
    preguntas_data = [
        {
            'texto_pregunta': '¿Qué es Python?',
            'tipo_pregunta': 'multiple',
            'puntaje': 1.0,
            'explicacion': 'Python es un lenguaje de programación interpretado de alto nivel y propósito general.',
            'respuestas': [
                {'texto': 'Un lenguaje de programación', 'correcta': True},
                {'texto': 'Una serpiente', 'correcta': False},
                {'texto': 'Un framework web', 'correcta': False},
                {'texto': 'Un sistema operativo', 'correcta': False},
            ]
        },
        {
            'texto_pregunta': '¿Django es un framework de Python?',
            'tipo_pregunta': 'verdadero_falso',
            'puntaje': 1.0,
            'explicacion': 'Django es un framework web de alto nivel escrito en Python.',
            'respuestas': [
                {'texto': 'Verdadero', 'correcta': True},
                {'texto': 'Falso', 'correcta': False},
            ]
        },
        {
            'texto_pregunta': '¿Cuál de los siguientes NO es un tipo de dato en Python?',
            'tipo_pregunta': 'multiple',
            'puntaje': 1.0,
            'explicacion': 'Los tipos de datos básicos en Python incluyen int, float, str, bool, list, tuple, dict, set.',
            'respuestas': [
                {'texto': 'integer', 'correcta': True},
                {'texto': 'int', 'correcta': False},
                {'texto': 'str', 'correcta': False},
                {'texto': 'bool', 'correcta': False},
            ]
        },
        {
            'texto_pregunta': '¿Qué es una API REST?',
            'tipo_pregunta': 'multiple',
            'puntaje': 1.0,
            'explicacion': 'REST (Representational State Transfer) es un estilo arquitectónico para diseñar servicios web.',
            'respuestas': [
                {'texto': 'Una interfaz de programación basada en HTTP', 'correcta': True},
                {'texto': 'Un lenguaje de programación', 'correcta': False},
                {'texto': 'Una base de datos', 'correcta': False},
                {'texto': 'Un editor de código', 'correcta': False},
            ]
        },
        {
            'texto_pregunta': '¿HTTP es un protocolo sin estado (stateless)?',
            'tipo_pregunta': 'verdadero_falso',
            'puntaje': 1.0,
            'explicacion': 'HTTP es un protocolo sin estado, lo que significa que cada petición es independiente.',
            'respuestas': [
                {'texto': 'Verdadero', 'correcta': True},
                {'texto': 'Falso', 'correcta': False},
            ]
        },
        {
            'texto_pregunta': '¿Cuál es el código de estado HTTP para "Recurso no encontrado"?',
            'tipo_pregunta': 'multiple',
            'puntaje': 1.0,
            'explicacion': '404 es el código de estado HTTP que indica que el recurso solicitado no fue encontrado.',
            'respuestas': [
                {'texto': '404', 'correcta': True},
                {'texto': '200', 'correcta': False},
                {'texto': '500', 'correcta': False},
                {'texto': '403', 'correcta': False},
            ]
        },
        {
            'texto_pregunta': '¿Qué es JSON?',
            'tipo_pregunta': 'multiple',
            'puntaje': 1.0,
            'explicacion': 'JSON (JavaScript Object Notation) es un formato ligero de intercambio de datos.',
            'respuestas': [
                {'texto': 'Un formato de intercambio de datos', 'correcta': True},
                {'texto': 'Un lenguaje de programación', 'correcta': False},
                {'texto': 'Una base de datos', 'correcta': False},
                {'texto': 'Un servidor web', 'correcta': False},
            ]
        },
        {
            'texto_pregunta': '¿SQL es un lenguaje de consulta estructurado?',
            'tipo_pregunta': 'verdadero_falso',
            'puntaje': 1.0,
            'explicacion': 'SQL significa Structured Query Language (Lenguaje de Consulta Estructurado).',
            'respuestas': [
                {'texto': 'Verdadero', 'correcta': True},
                {'texto': 'Falso', 'correcta': False},
            ]
        },
        {
            'texto_pregunta': '¿Qué es Git?',
            'tipo_pregunta': 'multiple',
            'puntaje': 1.0,
            'explicacion': 'Git es un sistema de control de versiones distribuido.',
            'respuestas': [
                {'texto': 'Un sistema de control de versiones', 'correcta': True},
                {'texto': 'Un lenguaje de programación', 'correcta': False},
                {'texto': 'Una base de datos', 'correcta': False},
                {'texto': 'Un framework web', 'correcta': False},
            ]
        },
        {
            'texto_pregunta': '¿CSS se usa para dar estilo a páginas web?',
            'tipo_pregunta': 'verdadero_falso',
            'puntaje': 1.0,
            'explicacion': 'CSS (Cascading Style Sheets) se utiliza para definir la presentación de documentos HTML.',
            'respuestas': [
                {'texto': 'Verdadero', 'correcta': True},
                {'texto': 'Falso', 'correcta': False},
            ]
        },
    ]
    
    preguntas_creadas = 0
    
    with transaction.atomic():
        for pregunta_data in preguntas_data:
            # Verificar si la pregunta ya existe
            if PreguntaDiagnostica.objects.filter(
                texto_pregunta=pregunta_data['texto_pregunta'],
                id_prueba__isnull=True
            ).exists():
                print(f"⚠️  Pregunta ya existe: {pregunta_data['texto_pregunta'][:50]}...")
                continue
            
            # Crear la pregunta sin prueba asociada (banco)
            pregunta = PreguntaDiagnostica.objects.create(
                id_prueba=None,  # Sin prueba = banco de preguntas
                texto_pregunta=pregunta_data['texto_pregunta'],
                tipo_pregunta=pregunta_data['tipo_pregunta'],
                puntaje=pregunta_data['puntaje'],
                explicacion=pregunta_data['explicacion'],
                estado=True
            )
            
            # Crear las respuestas
            for respuesta_data in pregunta_data['respuestas']:
                RespuestaDiagnostica.objects.create(
                    id_pregunta=pregunta,
                    texto_respuesta=respuesta_data['texto'],
                    es_correcta=respuesta_data['correcta']
                )
            
            preguntas_creadas += 1
            print(f"✅ Pregunta creada en banco: {pregunta.texto_pregunta[:50]}...")
    
    return preguntas_creadas


if __name__ == '__main__':
    print("=" * 70)
    print("🏦 CARGANDO PREGUNTAS AL BANCO DE PREGUNTAS")
    print("=" * 70)
    
    try:
        total = crear_preguntas_banco()
        print("\n" + "=" * 70)
        print(f"✅ PROCESO COMPLETADO: {total} preguntas creadas en el banco")
        print("=" * 70)
        
        # Mostrar estadísticas
        total_banco = PreguntaDiagnostica.objects.filter(id_prueba__isnull=True).count()
        print(f"\n📊 Total de preguntas en el banco: {total_banco}")
        
        multiple = PreguntaDiagnostica.objects.filter(
            id_prueba__isnull=True, 
            tipo_pregunta='multiple'
        ).count()
        verdadero_falso = PreguntaDiagnostica.objects.filter(
            id_prueba__isnull=True, 
            tipo_pregunta='verdadero_falso'
        ).count()
        
        print(f"   - Opción múltiple: {multiple}")
        print(f"   - Verdadero/Falso: {verdadero_falso}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
