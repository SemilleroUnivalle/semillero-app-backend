# Configuración de Gunicorn para producción

# Número de workers (procesos)
# Se recomienda 2-4 por núcleo de CPU
workers = 3

# Número de hilos por worker
threads = 2

# Dirección de enlace
bind = "0.0.0.0:8080"

# Timeout en segundos
timeout = 120

# Mantener workers activos por este tiempo
keepalive = 5

# Configuración de acceso a logs
accesslog = "-"  # Envía logs a stdout
errorlog = "-"  # Envía logs de error a stderr
loglevel = "info"

# Limitar el número máximo de conexiones simultáneas
max_requests = 1000
max_requests_jitter = 50

# Precargar aplicación para mejorar rendimiento
preload_app = True

# Configuración adicional recomendada para producción
worker_class = "sync"  # Puedes usar "gevent" o "uvicorn.workers.UvicornWorker" para más rendimiento
