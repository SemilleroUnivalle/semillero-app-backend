#!/bin/bash
# Script para cargar todos los datos de fixtures en el orden correcto
# Uso: bash fixtures/cargar_datos.sh

set -e  # Detener si hay algún error

echo "======================================"
echo "Iniciando carga de datos de fixtures"
echo "======================================"
echo ""

# Directorio de logs
LOG_DIR="/tmp/fixtures_logs"
mkdir -p $LOG_DIR

# Función para ejecutar un script de carga
ejecutar_carga() {
    local script=$1
    local nombre=$2
    
    echo "----------------------------------------"
    echo "[$nombre] Iniciando carga..."
    echo "----------------------------------------"
    
    python manage.py shell -c "exec(open('fixtures/$script').read()); main()" 2>&1 | tee "$LOG_DIR/$nombre.log"
    
    if [ $? -eq 0 ]; then
        echo "✓ [$nombre] Completado exitosamente"
    else
        echo "✗ [$nombre] Error en la carga"
        exit 1
    fi
    echo ""
}

# Orden de ejecución (respetando dependencias)
# 1. Áreas (no tiene dependencias)
ejecutar_carga "carga_area.py" "areas"

# 2. Categorías (no tiene dependencias)
ejecutar_carga "carga_categoria.py" "categorias"

# 3. Módulos (depende de áreas y categorías)
ejecutar_carga "carga_modulo.py" "modulos"

# 4. Oferta Académica (no tiene dependencias adicionales)
ejecutar_carga "carga_oferta_academica.py" "oferta_academica"

# 5. Oferta Categoría (depende de oferta académica, categoría y módulos)
ejecutar_carga "carga_oferta_categoria.py" "oferta_categoria"

# 6. Profesores (depende de usuarios)
ejecutar_carga "carga_profesor.py" "profesores"

# 7. Monitores académicos (depende de usuarios)
ejecutar_carga "carga_mon_academico.py" "monitores_academicos"

# 8. Acudientes (se carga con loaddata)
echo "----------------------------------------"
echo "[acudientes] Iniciando carga..."
echo "----------------------------------------"
python manage.py loaddata fixtures/acudientes.json 2>&1 | tee "$LOG_DIR/acudientes.log"
if [ $? -eq 0 ]; then
    echo "✓ [acudientes] Completado exitosamente"
else
    echo "✗ [acudientes] Error en la carga"
    exit 1
fi
echo ""

# 9. Estudiantes (depende de usuarios y acudientes)
ejecutar_carga "carga_estudiante.py" "estudiantes"

# 10. Matrículas (depende de estudiantes, módulos y ofertas)
ejecutar_carga "carga_matricula.py" "matriculas"

echo "======================================"
echo "Carga de datos completada exitosamente"
echo "======================================"
echo ""
echo "Logs guardados en: $LOG_DIR"
echo ""
echo "Resumen de archivos cargados:"
ls -lh $LOG_DIR
