# 🎯 Resumen: Implementación del Banco de Preguntas

## ✅ Cambios Realizados

### 1. **Modelo de Datos** (`models.py`)
- ✅ Campo `id_prueba` ahora es **opcional** (`null=True, blank=True`)
- ✅ Preguntas pueden existir sin estar asociadas a una prueba
- ✅ Actualizado el método `__str__` para mostrar `[Banco]` o `[Nombre Prueba]`
- ✅ Removido `unique_together` que causaba conflictos con valores NULL

### 2. **Serializers** (`serializers.py`)
- ✅ Agregado campo `id_prueba` al serializer de lectura
- ✅ Nuevo campo calculado `en_banco` que indica si la pregunta está en el banco
- ✅ Soporte completo para preguntas con y sin prueba asociada

### 3. **Vistas y Endpoints** (`views.py`)
Se agregaron **3 nuevos endpoints**:

#### 📋 GET `/preguntas/banco/`
- Lista todas las preguntas del banco (sin prueba asociada)
- Filtro opcional por `tipo_pregunta`
- Retorna preguntas con sus respuestas

#### 🔗 POST `/preguntas/asignar-a-prueba/`
- Asigna una pregunta del banco a una prueba específica
- La pregunta se **mueve** del banco a la prueba
- Validación: solo funciona con preguntas del banco

#### 📋 POST `/preguntas/clonar-del-banco/`
- **Clona** una pregunta del banco a una prueba
- La pregunta original **permanece** en el banco
- Copia también todas las respuestas
- Permite reutilización múltiple

### 4. **Documentación**
- ✅ Creado `BANCO_PREGUNTAS.md` con documentación completa
- ✅ Incluye ejemplos de uso, casos de uso y mejores prácticas
- ✅ Diagramas de flujo y comparaciones

### 5. **Fixtures y Scripts**
- ✅ Creado `carga_banco_preguntas.py` con 10 preguntas de ejemplo
- ✅ Actualizado `cargar_datos.ps1` para incluir carga del banco
- ✅ Preguntas sobre programación, web, bases de datos, etc.

---

## 🚀 Cómo Usar

### Crear una pregunta en el banco
```bash
POST /prueba_diagnostica/preguntas/crear-con-respuestas/
{
  "id_prueba": null,  # ← Clave: null = banco
  "texto_pregunta": "¿Qué es Python?",
  "tipo_pregunta": "multiple",
  "puntaje": 1.0,
  "respuestas": [...]
}
```

### Listar preguntas del banco
```bash
GET /prueba_diagnostica/preguntas/banco/
GET /prueba_diagnostica/preguntas/banco/?tipo_pregunta=multiple
```

### Asignar pregunta a una prueba (mover)
```bash
POST /prueba_diagnostica/preguntas/asignar-a-prueba/
{
  "id_pregunta": 15,
  "id_prueba": 3
}
```

### Clonar pregunta a una prueba (copiar)
```bash
POST /prueba_diagnostica/preguntas/clonar-del-banco/
{
  "id_pregunta": 15,
  "id_prueba": 3
}
```

---

## 📊 Estructura de Respuesta

Todas las preguntas ahora incluyen:
```json
{
  "id_pregunta": 15,
  "id_prueba": null,           // ← null = en banco
  "texto_pregunta": "...",
  "tipo_pregunta": "multiple",
  "en_banco": true,            // ← Campo calculado
  "respuestas": [...]
}
```

---

## 🔄 Flujos de Trabajo

### Flujo 1: Crear y Reutilizar
1. Crear pregunta con `id_prueba: null`
2. Pregunta queda en el banco
3. Clonar a múltiples pruebas según necesidad

### Flujo 2: Mover del Banco
1. Crear pregunta en el banco
2. Asignar a una prueba específica
3. Pregunta ya no está en el banco

### Flujo 3: Devolver al Banco
1. Hacer PATCH a la pregunta
2. Establecer `id_prueba: null`
3. Pregunta vuelve al banco

---

## 🎓 Casos de Uso

### ✅ Profesor con banco de preguntas
- Crea 100 preguntas sobre Python
- Las mantiene en el banco
- Para cada examen, clona las relevantes
- Puede modificar las copias sin afectar el original

### ✅ Preguntas comunes entre módulos
- Preguntas básicas de programación
- Se clonan a diferentes módulos
- Cada módulo puede ajustar según necesidad

### ✅ Versiones de exámenes
- Crear 3 versiones del mismo examen
- Clonar las mismas preguntas del banco
- Cambiar el orden en cada versión

---

## 📝 Notas Importantes

1. **Migración de Base de Datos**
   - Ya ejecutaste la migración en el contenedor ✅
   - El campo `id_prueba` ahora acepta NULL

2. **Compatibilidad**
   - Las preguntas existentes siguen funcionando
   - Solo las nuevas pueden estar en el banco
   - No afecta funcionalidad existente

3. **Validaciones**
   - Una pregunta solo puede tener una respuesta correcta
   - Al asignar, verifica que esté en el banco
   - Al clonar, copia todas las respuestas

---

## 🧪 Testing

### Cargar preguntas de ejemplo
```bash
# Desde el contenedor
python -m fixtures.carga_banco_preguntas

# O desde el script principal
.\fixtures\cargar_datos.ps1
```

### Verificar en Swagger
1. Ir a `/swagger/`
2. Buscar sección "prueba-diagnostica"
3. Probar endpoints:
   - `GET /preguntas/banco/`
   - `POST /preguntas/asignar-a-prueba/`
   - `POST /preguntas/clonar-del-banco/`

---

## 📚 Archivos Modificados/Creados

### Modificados
- ✅ `prueba_diagnostica/models.py`
- ✅ `prueba_diagnostica/serializers.py`
- ✅ `prueba_diagnostica/views.py`
- ✅ `fixtures/cargar_datos.ps1`

### Creados
- ✅ `prueba_diagnostica/BANCO_PREGUNTAS.md`
- ✅ `fixtures/carga_banco_preguntas.py`
- ✅ `prueba_diagnostica/RESUMEN_IMPLEMENTACION.md` (este archivo)

---

## 🎯 Próximos Pasos Sugeridos

1. **Frontend**
   - Crear interfaz para gestionar banco de preguntas
   - Botón "Agregar del banco" al crear pruebas
   - Vista de preguntas disponibles

2. **Mejoras Opcionales**
   - Categorías/etiquetas para preguntas del banco
   - Búsqueda y filtrado avanzado
   - Estadísticas de uso de preguntas
   - Versionado de preguntas

3. **Documentación**
   - Actualizar README principal
   - Agregar ejemplos de uso en Postman
   - Video tutorial (opcional)

---

## ✨ Beneficios Logrados

✅ **Reutilización**: Preguntas pueden usarse en múltiples pruebas  
✅ **Eficiencia**: No recrear preguntas similares  
✅ **Organización**: Banco centralizado de preguntas  
✅ **Flexibilidad**: Asignar o clonar según necesidad  
✅ **Escalabilidad**: Fácil agregar más preguntas  

---

**Implementado por**: Antigravity AI  
**Fecha**: 2025-12-11  
**Estado**: ✅ Completado y Funcional
