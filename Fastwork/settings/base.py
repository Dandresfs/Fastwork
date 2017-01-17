"""
Bolsa de Empleo Fast Work Colombia
"""

import os
from celery.schedules import crontab

# CELERY STUFF
BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Bogota'


CELERYBEAT_SCHEDULE = {
    're-send-email': {
        'task': 'accounts.tasks.re_send_mail',
        'schedule': crontab(),
        'args': (),
    },
}


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_REDIRECT_URL = '/ofertas/'
LOGIN_URL = '/ofertas/'
LOGOUT_URL = '/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wpytn67x61&8b&#yvb70r*6la@1i-57eii*bl+b7p9is3@(k&e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMINS = [('DIEGO','sistemas@asoandes.org')]

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('fastworkcolombia')
EMAIL_PORT = os.getenv('EMAIL_PORT')
DEFAULT_FROM_EMAIL = 'Fast Work Colombia<no-responder@fastworkcolombia.com>'
EMAIL_USE_TLS = True


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'accounts',
    'hv',
    'rest',
    'empresa',
    'ofertas'
]

THIRD_PARTY_APPS = [
    'django_cleanup',
    'social.apps.django_app.default',
    'crispy_forms',
    'rest_framework',
    'mail_templated',
    'django_tables2',
    'django_filters'
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Fastwork.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '../templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media',
                # Python Social Auth Context Processors
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Facebook
    'social.backends.facebook.FacebookOAuth2',
    # Twitter
    'accounts.backends.TwitterOAuth',
    # Linkedin
    'social.backends.linkedin.LinkedinOAuth2',
    # Google
    'social.backends.google.GoogleOAuth2',
    # Django
    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'Fastwork.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../static'),
)


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../media')



SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is were emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social.pipeline.user.get_username',
    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    # Create the record that associated the social account with this user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'accounts.pipeline.user_details',
    'accounts.pipeline.save_profile_picture',
)

SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'es_CO',
  'fields': 'id, name, email, age_range'
}

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = os.getenv('LINKEDIN_KEY')
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = os.getenv('LINKEDIN_SECRET')
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_emailaddress','r_basicprofile']
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email-address','picture-urls::(original)',]
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [('emailAddress', 'email_address'),('picture-url', 'picture_url')]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_TWITTER_KEY = os.getenv('TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = os.getenv('TWITTER_SECRET')

SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/ofertas/"
SOCIAL_AUTH_LOGIN_URL = "/ofertas/"


SOCIAL_AUTH_EMAIL_FORM_URL = '/login-email/'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'home.html'

AUTH_USER_MODEL = "accounts.User"

MERCADOPAGO_CLIENT_ID = os.getenv('MERCADOPAGO_CLIENT_ID')
MERCADOPAGO_SECRET_KEY = os.getenv('MERCADOPAGO_SECRET_KEY')
VALOR_EMPRESA = 100000
VALOR_OFERTA = 186000