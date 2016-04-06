from Fastwork.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = 'staticfiles'


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('FASTWORK_DB_NAME'),

            'USER': os.getenv('FASTWORK_DB_USER'),
            'PASSWORD': os.getenv('FASTWORK_DB_PASSWORD'),
            'HOST': os.getenv('FASTWORK_DB_HOST'),
            'PORT': os.getenv('FASTWORK_DB_PORT'),
        }
}