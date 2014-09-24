import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

ROOT_URLCONF = 'preguntas.urls'
WSGI_APPLICATION = 'preguntas.wsgi.application'

LANGUAGE_CODE = 'es-PE'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'
LOGIN_URL = '/admin/'