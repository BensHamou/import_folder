from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

AUTHENTICATION_BACKENDS = [
    'account.authentication.ApiBackend',
    'django.contrib.auth.backends.ModelBackend',
    ]

with open(os.path.join(BASE_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

DEBUG = True

swappable = 'AUTH_USER_MODEL'

AUTH_USER_MODEL = 'account.User'

ADMIN_URL = 'puma_import_folder/admin/'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "account",
    "report",
    "django.contrib.humanize",
    'bootstrap5',
    'fontawesomefree',
    'django_filters',
    'widget_tweaks',
    'django_extensions',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "import_folder.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [os.path.join(BASE_DIR, 'account', 'templates', 'user'), os.path.join(BASE_DIR, 'account', 'templates', 'fragment'), 
                 os.path.join(BASE_DIR, 'account', 'templates', 'site'), os.path.join(BASE_DIR, 'account', 'templates', 'currency'),
                 os.path.join(BASE_DIR, 'report', 'templates', 'report'), os.path.join(BASE_DIR, 'report', 'templates', 'emplacement'),
                 os.path.join(BASE_DIR, 'report', 'templates', 'transitor')
                 ],        
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "import_folder.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    } 
    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql',
    #    'NAME': 'ImportDB',
    #    'USER': 'import_report',
    #    'PASSWORD': 'import_report',
    #    'HOST': '10.10.10.53',
    #    'PORT': '5422',
    #}
    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql',
    #    'NAME': 'ImportFolderDB',
    #    'USER': 'puma_prod',
    #    'PASSWORD': 'puma_prod',
    #    'HOST': '10.10.10.101',
    #    'PORT': '5434',
    #}   
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "fr"

TIME_ZONE = "Africa/Algiers"

USE_I18N = True

USE_TZ = True

LOGIN_REDIRECT_URL = 'login_success'
LOGOUT_REDIRECT_URL = '/login'

STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_HOST_USER = "pumafimport@outlook.com"
EMAIL_HOST_PASSWORD = "puma_import22!"