import os
from pathlib import Path 
 

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent 

# Secret Key
SECRET_KEY = 'django-insecure-=vex5-bxolz-7_$9l71&_zufoe@2f3v-^*9+uuhdgu8-g2q*en'

# Debug Mode
DEBUG = False

# Allowed Hosts
ALLOWED_HOSTS = ["*"]

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'storages',
    "corsheaders",
]
CORS_ALLOW_ALL_ORIGINS = True
# Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'StudentLiving.urls'
# LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'StudentLiving.wsgi.application'
 

# Database Settings
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Email Settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" 
EMAIL_HOST_USER = "kgaogelodeveloper@gmail.com"
EMAIL_HOST_PASSWORD = "ornq pfjn cbga iykr"
DEFAULT_FROM_EMAIL = "kgaogelodeveloper@gmail.com"

EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = 587
EMAIL_USE_TLS = True 
# AWS S3 Storage Settings 

 
STATIC_URL = '/static/'
# STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'
MEDIA_URL = '/media/'


# Static and Media
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'home/static'),)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'home.authentication.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
