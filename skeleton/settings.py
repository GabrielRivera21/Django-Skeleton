import os

from configurations import Configuration, values


class Common(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    ENVIRONMENT = values.Value(environ_prefix=None, default='DEVELOPMENT')

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    TEMPLATE_DEBUG = values.BooleanValue(DEBUG)

    ALLOWED_HOSTS = ['*']

    # Application definition
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
        'django.contrib.sites',

        # Third party
        'django_extensions',
        'corsheaders',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',

        # Apps
        'skeleton.users',
    )

    MIDDLEWARE_CLASSES = (
        'djangosecure.middleware.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'skeleton.urls'

    WSGI_APPLICATION = 'skeleton.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.7/ref/settings/#databases
    DATABASES = values.DatabaseURLValue(
        'sqlite:///{}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
    )

    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/
    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.7/howto/static-files/
    MEDIA_ROOT = 'media'
    MEDIA_URL = '/media/'

    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

    TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

    AUTH_USER_MODEL = 'users.User'

    # auth and allauth settings
    LOGIN_REDIRECT_URL = '/'
    LOGIN_URL = '/accounts/login/'
    ACCOUNT_EMAIL_VERIFICATION = 'optional'
    ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Skeleton] '
    ACCOUNT_LOGOUT_ON_GET = True
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_CONFIRM_EMAIL_ON_GET = True
    ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_URL
    ACCOUNT_USERNAME_BLACKLIST = ['admin']
    ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
    ACCOUNT_SIGNUP_FORM_CLASS = 'skeleton.users.forms.SignupForm'
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    ACCOUNT_USERNAME_REQUIRED = False

    TEMPLATE_CONTEXT_PROCESSORS = (
        # Django Default
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.request",
        "django.contrib.messages.context_processors.messages",
    )

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    )

    SOCIALACCOUNT_PROVIDERS = \
        {'facebook':
            {
                'METHOD': 'oauth2',
                'SCOPE': ['email', 'public_profile'],
                'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
                'FIELDS': [
                    'id',
                    'email',
                    'name',
                    'first_name',
                    'last_name',
                    'verified',
                    'locale',
                    'timezone',
                    'link',
                    'gender',
                    'updated_time'],
                'EXCHANGE_TOKEN': True,
                'LOCALE_FUNC': lambda request: 'en_US',
                'VERIFIED_EMAIL': False,
                'VERSION': 'v2.5'
            }
         }

    SITE_ID = 1

    PROTOCOL = 'http'

    DOMAIN = values.Value(environ_prefix=None)

    SITE_NAME = values.Value(environ_prefix=None)

    DEFAULT_FROM_EMAIL = values.Value()
    EMAIL_HOST = values.Value()
    EMAIL_HOST_USER = values.Value()
    EMAIL_HOST_PASSWORD = values.Value()
    EMAIL_PORT = values.IntegerValue()
    EMAIL_USE_TLS = values.BooleanValue(False)


class Development(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True

    TEMPLATE_DEBUG = True

    ALLOWED_HOSTS = []

    INSTALLED_APPS = Common.INSTALLED_APPS + (
        'debug_toolbar',
    )

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    DEBUG_TOOLBAR_PATCH_SETTINGS = values.BooleanValue(True)


class Staging(Common):
    """
    The in-staging settings.
    """
    INSTALLED_APPS = Common.INSTALLED_APPS + (
        'djangosecure',
    )

    # django-secure
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    SECURE_HSTS_SECONDS = values.IntegerValue(31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_FRAME_DENY = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_PROXY_SSL_HEADER = values.TupleValue(
        ('HTTP_X_FORWARDED_PROTO', 'https')
    )

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    PROTOCOL = 'https'


class Production(Staging):
    """
    The in-production settings.
    """
    pass
