# Configuración de Gunicorn para producción

# Número de workers (procesos)
# Se recomienda 2-4 por núcleo de CPU
workers = 3

# Número de hilos por worker
threads = 2

# Dirección de enlace
# Configuración de Gunicorn para producción

# Número de workers (procesos)
# Se recomienda 2-4 por núcleo de CPU
workers = 3

# Número de hilos por worker
threads = 2

# Dirección de enlace
bind = "0.0.0.0:8080"
workers = 3