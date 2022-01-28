import dj_database_url
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv('SECRET_KEY', 'PlaceholderSecretKey')
DEBUG = os.getenv('DEBUG', False) == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', False) == 'True'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', False) == 'True'
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', False) == 'True'
SECURE_REFERRER_POLICY = os.getenv('SECURE_REFERRER_POLICY', None) == 'True'
SECURE_HSTS_SECONDS = os.getenv('SECURE_HSTS_SECONDS', 0)
if not DEBUG:
    ALLOWED_HOSTS = os.getenv('ALLOWED_DOMAINS', '').split(',')
else:
    ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party applications:
    'django_extensions',
    'reversion',
    'mptt',
    'leaflet',
    'crispy_forms',
    'webtemplate_dbca',
    'bootstrap_pagination',
    # Project applications:
    'nomenclature',
    'herbarium',
    'naturemap',
    'crossreference',
    'graphic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dbca_utils.middleware.SSOLoginMiddleware',
]

ROOT_URLCONF = 'waherb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(BASE_DIR, 'waherb', 'templates'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'waherb.context_processors.from_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'waherb.wsgi.application'


DATABASES = {
    'default': dj_database_url.config(),
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Australia/Perth'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Media uploads
# Ensure that the media directory exists:
if not os.path.exists(os.path.join(BASE_DIR, 'media')):
    os.mkdir(os.path.join(BASE_DIR, 'media'))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# crispy_forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = False


# Spatial service URLs
GEOSERVER_WMS_URL = os.getenv('GEOSERVER_WMS_URL', '')
GEOSERVER_WMTS_URL = os.getenv('GEOSERVER_WMTS_URL', '')


# Site settings
ENVIRONMENT_NAME = os.getenv('ENVIRONMENT_NAME', '')
ENVIRONMENT_COLOUR = os.getenv('ENVIRONMENT_COLOUR', '')
