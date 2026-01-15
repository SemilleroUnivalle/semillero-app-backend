# Script PowerShell para cargar todos los datos de fixtures en el orden correcto
# Uso: .\fixtures\cargar_datos.ps1

$ErrorActionPreference = "Stop"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Iniciando carga de datos de fixtures" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Función para ejecutar un script de carga dentro del contenedor
function Ejecutar-Carga {
    param(
        [string]$Script,
        [string]$Nombre
    )
    
    Write-Host "----------------------------------------" -ForegroundColor Yellow
    Write-Host "[$Nombre] Iniciando carga..." -ForegroundColor Yellow
    Write-Host "----------------------------------------" -ForegroundColor Yellow
    
    $comando = "python manage.py shell -c `"exec(open('fixtures/$Script').read()); main()`" 2>&1 | tee /tmp/$Nombre.log"
    
    docker exec semillero_backend bash -c $comando
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ [$Nombre] Completado exitosamente" -ForegroundColor Green
    } else {
        Write-Host "✗ [$Nombre] Error en la carga" -ForegroundColor Red
        exit 1
    }
    Write-Host ""
}

# Orden de ejecución (respetando dependencias)
# 1. Áreas (no tiene dependencias)
Ejecutar-Carga "carga_area.py" "areas"

# 2. Categorías (no tiene dependencias)
Ejecutar-Carga "carga_categoria.py" "categorias"

# 3. Módulos (depende de áreas y categorías)
Ejecutar-Carga "carga_modulo.py" "modulos"

# 4. Oferta Académica (no tiene dependencias adicionales)
Ejecutar-Carga "carga_oferta_academica.py" "oferta_academica"

# 5. Oferta Categoría (depende de oferta académica, categoría y módulos)
Ejecutar-Carga "carga_oferta_categoria.py" "oferta_categoria"

# 6. Profesores (depende de usuarios)
Ejecutar-Carga "carga_profesor.py" "profesores"

# 7. Monitores académicos (depende de usuarios)
Ejecutar-Carga "carga_mon_academico.py" "monitores_academicos"

# 8. Acudientes (se carga con loaddata)
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host "[acudientes] Iniciando carga..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

$comando = "python manage.py loaddata fixtures/acudientes.json 2>&1 | tee /tmp/acudientes.log"
docker exec semillero_backend bash -c $comando

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ [acudientes] Completado exitosamente" -ForegroundColor Green
} else {
    Write-Host "✗ [acudientes] Error en la carga" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 9. Estudiantes (depende de usuarios y acudientes)
Ejecutar-Carga "carga_estudiante.py" "estudiantes"

# 10. Banco de Preguntas (opcional - preguntas reutilizables sin prueba asociada)
Ejecutar-Carga "carga_banco_preguntas.py" "banco_preguntas"

# 11. Matrículas (depende de estudiantes, módulos y ofertas)
Ejecutar-Carga "carga_matricula.py" "matriculas"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Carga de datos completada exitosamente" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Logs guardados en el contenedor en: /tmp/" -ForegroundColor Gray
