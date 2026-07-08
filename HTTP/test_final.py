"""
Script que obtiene el token desde Django ORM y ejecuta la prueba del endpoint.
Se copia al contenedor y se ejecuta ahi.
"""
import subprocess
import json
import sys
import io

# Obtener token desde Django
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semillero_backend.settings')
django.setup()

from rest_framework.authtoken.models import Token
from cuenta.models import CustomUser
import urllib.request

u = CustomUser.objects.filter(user_type='administrador').first()
if not u:
    print("No hay usuario administrador")
    sys.exit(1)

t, _ = Token.objects.get_or_create(user=u)
TOKEN = t.key

print(f"Admin: {u.email}")
print(f"Token: {TOKEN[:10]}...{TOKEN[-5:]}")

# Crear Excel en memoria
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws.append(["documento","nombre","modulo","docente","monitor",
           "nota_modulo","nota_docente","nota_monitor","nota_estudiante","comentarios"])

# Fila 1: doc '200' (Mateo Navarro) - debe crear encuesta
ws.append(["200","Mateo Navarro","Matematicas","Carlos Gomez","Laura Diaz",4.5,4.7,4.3,4.8,"Excelente"])
# Fila 2: doc '201' (Carlos Lopez) - debe crear encuesta
ws.append(["201","Carlos Lopez","Fisica","Pedro Ruiz","Maria Torres",3.0,4.0,3.5,4.2,"Buen semestre"])
# Fila 3: doc inexistente - debe dar error
ws.append(["9999999999","Fantasma","N/A","N/A","N/A",3.0,3.0,3.0,3.0,""])
# Fila 4: nota fuera de rango - debe dar error
ws.append(["200","Mateo","Mat","Prof","Mon",6.0,4.0,3.0,4.0,""])

buf = io.BytesIO()
wb.save(buf)
buf.seek(0)
file_data = buf.read()

print(f"\nExcel generado: {len(file_data)} bytes, {ws.max_row - 1} filas de datos")

# Llamar al endpoint
URL = "http://localhost:8080/encuesta_satisfaccion/encuesta/cargar-excel/"
BOUNDARY = "TestBoundary99XYZ"
CRLF = b"\r\n"

header_part = (
    b"--" + BOUNDARY.encode() + CRLF
    + b'Content-Disposition: form-data; name="archivo"; filename="test.xlsx"' + CRLF
    + b"Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" + CRLF
    + CRLF
)
body = header_part + file_data + CRLF + b"--" + BOUNDARY.encode() + b"--" + CRLF

req = urllib.request.Request(
    URL,
    data=body,
    headers={
        "Authorization": "Token " + TOKEN,
        "Content-Type": "multipart/form-data; boundary=" + BOUNDARY,
    },
    method="POST",
)

print(f"\nPOST {URL}")
print("-" * 60)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("\n" + "=" * 60)
        print("RESUMEN")
        print(f"  Total filas  : {result['total_filas']}")
        print(f"  Creadas      : {result['creadas']}")
        print(f"  Actualizadas : {result['actualizadas']}")
        print(f"  Errores      : {result['errores']}")
        if result.get("detalle_exito"):
            print("\n  Exitos:")
            for e in result["detalle_exito"]:
                print(f"    Fila {e['fila']} | {e['documento']} - {e['nombre']} | {e['accion']} | {e['notas_guardadas']}")
        if result.get("detalle_errores"):
            print("\n  Errores:")
            for e in result["detalle_errores"]:
                print(f"    Fila {e['fila']} | {e['documento']} | {e['error']}")

except urllib.error.HTTPError as exc:
    body_err = exc.read().decode("utf-8")
    print(f"HTTP {exc.code}: {body_err[:500]}")
except Exception as exc:
    print(f"Error: {exc}")
