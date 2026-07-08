# Reporte de Evidencias: Suite de Pruebas de Integración (API y Endpoints)

Este documento detalla el diseño, la estructura y los resultados de la suite de pruebas de integración automatizadas implementadas para validar el comportamiento del backend de la aplicación de extremo a extremo (End-to-End).

## 1. Diseño del Entorno de Pruebas de Integración

A diferencia de las pruebas unitarias, las pruebas de integración validan que el sistema de enrutamiento (URLs), la autenticación de usuarios, el control de permisos (Roles), los serializadores y la persistencia en la base de datos funcionen en conjunto. 

La suite se implementó utilizando el cliente de pruebas HTTP **`APIClient`** provisto por Django REST Framework, simulando peticiones de red reales tal como lo haría el Frontend de la aplicación.

---

## 2. Flujos Críticos de Negocio Evaluados

Se crearon 5 archivos de prueba modularizados dentro del directorio `integration_tests/` para evaluar de manera integral los procesos clave del sistema:

### A. Autenticación y Control de Accesos (`integration_tests/test_autenticacion.py`)
* **Login Exitoso**: Valida que al enviar un número de documento y contraseña válidos al endpoint `/login/`, el sistema retorne el token JWT de sesión, el rol del usuario y su ID específico.
* **Credenciales Inválidas**: Verifica el rechazo seguro y el código `401 Unauthorized` al intentar ingresar con credenciales incorrectas.
* **Logout Exitoso**: Comprueba que el endpoint `/logout/` destruya de forma segura el token activo.
* **Acceso Protegido**: Valida que un usuario anónimo (sin token) sea rechazado automáticamente con código `401` al intentar acceder a rutas restringidas (como el listado de áreas `/area/are/`).

### B. Ciclo de Matrícula e Inscripción (`integration_tests/test_flujo_inscripcion.py`)
* **Registro de Estudiantes**: Simula a un usuario ingresando al sistema por primera vez, enviando sus datos personales y los de su acudiente al endpoint abierto `/estudiante/est/`.
* **Inscripción a Módulo**: Valida que el estudiante pueda inscribirse a un módulo académico activo (`POST /inscripcion/`), verificando que el sistema controle que la oferta académica y la categoría estén vigentes antes de persistir la inscripción en la base de datos.

### C. Gestión y Seguimiento Académico (`integration_tests/test_gestion_academica.py`)
* **Registro de Asistencias**: Verifica que un profesor autenticado pueda registrar la asistencia diaria de los estudiantes de su grupo asignado a través de `/asistencia/asis/`.
* **Carga de Calificaciones**: Comprueba que el docente pueda registrar notas de seguimiento y conceptuales en `/seguimiento_academico/seg/`, validando que el backend calcule la nota final del estudiante en tiempo real mediante fórmulas matemáticas preestablecidas.
* **Denegación de Permisos**: Asegura que un estudiante que intente modificar sus calificaciones sea bloqueado de inmediato con un código de respuesta `403 Forbidden`.

### D. Procesamiento de Pagos (`integration_tests/test_flujo_pagos.py`)
* **Creación de Pagos**: Valida que un estudiante pueda cargar y registrar el soporte digital de su pago (`POST /pago/pago/`) adjuntando el enlace de su comprobante en PDF.
* **Restricción de Reportes**: Verifica que solo los administradores puedan visualizar el consolidado de pagos (`GET /pago/pago/`), restringiendo esta consulta a los estudiantes con un código `403`.

### E. Encuestas de Satisfacción (`integration_tests/test_evaluaciones_encuestas.py`)
* **Evaluación del Estudiante**: Valida que un estudiante registre la encuesta de satisfacción sobre las clases y el monitor (`POST /encuesta_satisfaccion/encuesta/`).
* **Seguridad de Datos**: Comprueba que un estudiante no pueda responder ni modificar la encuesta de otro estudiante del sistema.
* **Reporte de Calidad**: Asegura que el personal docente y administrativo pueda acceder al reporte completo de encuestas (`GET /encuesta_satisfaccion/encuesta/reporte/`) para el control de calidad del programa.

---

## 3. Resultados de la Ejecución

Toda la suite de integración fue validada y ejecutada dentro del contenedor Docker del backend (`semillero_backend`) conectado a la base de datos de pruebas. Las 8 pruebas de integración críticas pasaron exitosamente.

### Resultados Consolidados del Terminal:
* **Pruebas ejecutadas**: 8
* **Pruebas aprobadas**: 8 (100% de éxito)
* **Cobertura de código**: Reporte consolidado de cobertura HTML actualizado.

```bash
root@semillero_backend:/app# pytest integration_tests/
============================= test session starts ==============================
platform linux -- Python 3.10.19, pytest-8.3.5, pluggy-1.5.0
django: version: 5.0.14, settings: semillero_backend.settings (from ini)
rootdir: /app
configfile: pytest.ini
testpaths: .
plugins: anyio-4.11.0, django-4.10.0, cov-6.0.0
collected 8 items

integration_tests/test_autenticacion.py ....                             [ 50%]
integration_tests/test_evaluaciones_encuestas.py .                       [ 62%]
integration_tests/test_flujo_inscripcion.py .                            [ 75%]
integration_tests/test_flujo_pagos.py .                                  [ 87%]
integration_tests/test_gestion_academica.py .                            [100%]

======================== 8 passed, 2 warnings in 14.59s ========================
```
