"""
Django settings for semillero_backend project.

Generated by 'django-admin startproject' using Django 5.1.7.

Para más información sobre este archivo, consulta
https://docs.djangoproject.com/en/5.1/topics/settings/

Para la lista completa de configuraciones y sus valores, consulta
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
# Construye rutas dentro del proyecto como esta: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Configuración rápida para desarrollo - no apta para producción
# Consulta https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: mantén la clave secreta usada en producción en secreto
SECRET_KEY = 'django-insecure-3-!4cm82i1-s5hbg4*m_4x!=wg=lj1$0(-3hb&awt2^0nzpp@o'

# ADVERTENCIA DE SEGURIDAD: no ejecutes con debug activado en producción
DEBUG = True

ALLOWED_HOSTS = [
    'ec2-54-234-86-157.compute-1.amazonaws.com',
    '54.234.86.157',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    #ip publica servidor aws
    # otros hosts permitidos...
]

# Definición de aplicaciones

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'psycopg2',
    'estudiante',
    'acudiente',
    'area',
    'asistencia',
    'discapacidad',
    'evaluacion_programa',
    'grado_escolar',
    'grupo',
    'historial_cambios',
    'inscripcion',
    'modulo',
    'oferta_modulo',
    'pago',
    'periodo_academico',
    'seguimiento_academico'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'semillero_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Asegúrate de incluir esta línea
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'semillero_backend.wsgi.application'

# Base de datos
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'database_semillero',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'semillero-database',
        'USER': 'semillero',
        'PASSWORD': 'adminsemillero',
        'HOST': 'database-semillero.cktk40yw6g7t.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    },
}
"""
# Validación de contraseñas
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internacionalización
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'  # URL base para acceder a los archivos estáticos
STATICFILES_DIRS = [BASE_DIR / 'static']  # Ubicaciones adicionales para buscar archivos
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Donde se recolectan todos los archivos en producción

# Tipo de campo de clave primaria predeterminado
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de CORS
# Define la lista de orígenes permitidos para solicitudes de origen cruzado
CORS_ALLOWED_ORIGINS = [
    "http://191.104.218.125" #PC Alejandro
    "http://181.78.17.229" #PC Sebastian
    "http://localhost:8080",  # Servidor de desarrollo local
    "http://127.0.0.1:8000",  # Localhost con el puerto predeterminado de Django
    "http://127.0.0.1:3000",
]

# Especifica los métodos HTTP permitidos para solicitudes de origen cruzado
CORS_ALLOW_METHODS = [
    "DELETE",  # Permitir solicitudes DELETE
    "GET",     # Permitir solicitudes GET
    "OPTIONS", # Permitir solicitudes OPTIONS
    "PATCH",   # Permitir solicitudes PATCH
    "POST",    # Permitir solicitudes POST
    "PUT",     # Permitir solicitudes PUT
]

# Especifica los encabezados HTTP permitidos en solicitudes de origen cruzado
CORS_ALLOW_HEADERS = [
    "accept",            # Encabezado Accept
    "accept-encoding",   # Encabezado Accept-Encoding
    "authorization",     # Encabezado Authorization
    "content-type",      # Encabezado Content-Type
    "dnt",               # Encabezado Do Not Track
    "origin",            # Encabezado Origin
    "user-agent",        # Encabezado User-Agent
    "x-csrftoken",       # Encabezado CSRF token
    "x-requested-with",  # Encabezado X-Requested-With
]

# Permitir todos los orígenes para solicitudes de origen cruzado (anula CORS_ALLOWED_ORIGINS)
CORS_ALLOW_ALL_ORIGINS = True