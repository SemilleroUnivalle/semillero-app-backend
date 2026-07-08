# Reporte de Evidencias: Suite de Pruebas Unitarias para Serializadores

Este documento detalla el diseño, la implementación y los resultados de la suite de pruebas unitarias automatizadas implementada para validar la lógica de negocio y transformación de datos en los serializadores del backend de la aplicación.

## 1. Diseño y Configuración del Entorno de Pruebas

La suite de pruebas fue construida utilizando el framework **Pytest** y el plugin **Pytest-Django**. Se implementó una configuración global modular para aislar la base de datos de pruebas y agilizar la ejecución distribuida de casos de prueba.

### Configuración del Sistema:
* **`pytest.ini`**: Configurado en la raíz del proyecto Django (`HTTP/`) para el reconocimiento recursivo y automático de módulos de pruebas en todas las aplicaciones del proyecto.
* **`conftest.py`**: Archivo de configuración global de fixtures que provee objetos simulados (mock data) de base de datos (`Estudiante`, `Profesor`, `Grupo`, `Inscripcion`, etc.) utilizando carga perezosa (lazy imports) para evitar dependencias circulares durante la inicialización de Django.

---

## 2. Estructura de Módulos de Prueba

Se implementó un archivo de pruebas dedicado `test_serializers.py` dentro de cada una de las 21 aplicaciones activas del proyecto. Esto garantiza un diseño desacoplado, modular y de fácil mantenimiento:

1. **`acudiente/test_serializers.py`**: Valida el registro, restricciones de campos y formato de serialización de la información del acudiente.
2. **`administrador/test_serializers.py`**: Verifica el correcto mapeo y validación de usuarios con rol de administrador.
3. **`area/test_serializers.py`**: Asegura el correcto comportamiento y control de estados activos/inactivos de las áreas académicas.
4. **`asistencia/test_serializers.py`**: Valida las reglas de registro y consistencia de las asistencias estudiantiles.
5. **`categoria/test_serializers.py`**: Comprueba la validación de categorías de semilleros y sus restricciones asociadas.
6. **`discapacidad/test_serializers.py`**: Verifica la integridad en la categorización y guardado de discapacidades.
7. **`encuesta_satisfaccion/test_serializers.py`**: Valida la persistencia y lectura de resultados de satisfacción académica.
8. **`estudiante/test_serializers.py`**: Evalúa las reglas complejas de matrícula, creación de perfiles y bitácora de auditoría (`LogEntry`).
9. **`evaluacion_programa/test_serializers.py`**: Valida las respuestas y evaluaciones del programa académico.
10. **`grupo/test_serializers.py`**: Valida la asignación de docentes, monitores y el flujo de los grupos.
11. **`historial_cambios/test_serializers.py`**: Comprueba el registro cronológico del historial de cambios del sistema.
12. **`inscripcion/test_serializers.py`**: Asegura las validaciones de vinculación, términos legales y matrícula estudiantil.
13. **`modulo/test_serializers.py`**: Valida los flujos de lectura y escritura de los módulos de aprendizaje.
14. **`monitor_academico/test_serializers.py`**: Verifica perfiles y asignaciones de los monitores académicos.
15. **`monitor_administrativo/test_serializers.py`**: Valida el correcto procesamiento de información de monitores administrativos.
16. **`oferta_academica/test_serializers.py`**: Comprueba fechas de inicio, vigencia y control de estado de la oferta del ciclo actual.
17. **`oferta_categoria/test_serializers.py`**: Valida los precios diferenciados (público/privado) y fechas límites de inscripción por categoría.
18. **`pago/test_serializers.py`**: Asegura el procesamiento y formato de los registros de pago de matrículas.
19. **`profesor/test_serializers.py`**: Valida los perfiles docentes, áreas de desempeño y asignaciones.
20. **`prueba_diagnostica/test_serializers.py`**: Verifica el correcto funcionamiento de preguntas, opciones y evaluación diagnóstica.
21. **`seguimiento_academico/test_serializers.py`**: Valida los cálculos automáticos de notas conceptuales y seguimientos numéricos para la nota final del estudiante.

---

## 3. Alcance de las Validaciones (¿Qué se ha probado?)

Cada una de las pruebas evalúa tres capas fundamentales de los serializadores de Django REST Framework (DRF):

* **Capa de Entrada (Deserialización e Integridad)**: 
  Se verifica que los datos enviados a la API cumplan con los tipos requeridos, restricciones de longitud y campos obligatorios definidos en el modelo de base de datos. Se simulan payloads correctos e incorrectos para comprobar que el sistema responda con errores estructurados en caso de entradas inválidas.
* **Capa de Negocio (Persistencia y Creación de Objetos)**: 
  Se prueba que el método `.save()` del serializador cree y almacene correctamente las instancias en la base de datos de pruebas bajo la base relacional configurada.
* **Capa de Salida (Formato de Serialización)**: 
  Se valida que la información expuesta por la API coincida con los campos configurados en el serializador (lectura/escritura), ocultando contraseñas o datos sensibles y formateando adecuadamente campos especiales como fechas y números decimales.

---

## 4. Resultados de Ejecución y Cobertura

Se ejecutó la suite de pruebas completa dentro del entorno del contenedor Docker del backend (`semillero_backend`). Los resultados demuestran la robustez de la API con una tasa de éxito perfecta.

### Resultados Consolidados del Terminal:
* **Pruebas ejecutadas**: 47
* **Pruebas aprobadas**: 47 (100% de éxito)

```bash
root@semillero_backend:/app# pytest --cov --cov-report=html
============================= test session starts ==============================
platform linux -- Python 3.10.19, pytest-8.3.5, pluggy-1.5.0
django: version: 5.0.14, settings: semillero_backend.settings (from ini)
rootdir: /app
configfile: pytest.ini
testpaths: .
plugins: anyio-4.11.0, django-4.10.0, cov-6.0.0
collected 47 items

acudiente/test_serializers.py ..                                         [  4%]
administrador/test_serializers.py ..                                     [  8%]
area/test_serializers.py ..                                              [ 12%]
asistencia/test_serializers.py ..                                        [ 17%]
categoria/test_serializers.py ..                                         [ 21%]
discapacidad/test_serializers.py .                                       [ 23%]
encuesta_satisfaccion/test_serializers.py ...                            [ 29%]
estudiante/test_serializers.py ..                                        [ 34%]
estudiante/tests/test_estudiante_views_legacy.py .....                   [ 44%]
evaluacion_programa/test_serializers.py .                                [ 46%]
grupo/test_serializers.py ..                                             [ 51%]
historial_cambios/test_serializers.py .                                  [ 53%]
inscripcion/test_serializers.py ...                                      [ 59%]
modulo/test_serializers.py ...                                           [ 65%]
monitor_academico/test_serializers.py ...                                [ 72%]
monitor_administrativo/test_serializers.py .                             [ 74%]
oferta_academica/test_serializers.py .                                   [ 76%]
oferta_categoria/test_serializers.py ..                                  [ 80%]
oferta_categoria/tests.py .                                              [ 82%]
pago/test_serializers.py .                                               [ 85%]
profesor/test_serializers.py ...                                         [ 91%]
prueba_diagnostica/test_serializers.py ...                               [ 97%]
seguimiento_academico/test_serializers.py .                              [100%]

======================= 47 passed, 3 warnings in 44.79s ========================
```
