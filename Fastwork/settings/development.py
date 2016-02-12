from Fastwork.settings.base import *

MEDIA_ROOT = os.path.join(BASE_DIR, '../media')

INSTALLED_APPS += (
    'debug_toolbar',
)

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}