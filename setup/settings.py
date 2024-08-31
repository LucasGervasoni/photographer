from pathlib import Path, os
from django.conf import settings
from dotenv import load_dotenv
import django_heroku
import dj_database_url

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.pages.apps.PagesConfig',
    'apps.users.apps.UsersConfig',
    'apps.main_crud.apps.MainCrudConfig',
    'apps.pictures.apps.PicturesConfig',
    'apps.search_location.apps.SearchLocationConfig',
    'rangefilter',
    "crispy_forms",
    "crispy_bootstrap4",
    "import_export",
    "storages",
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.pictures.middlewares.LargeFileUploadMiddleware',
    'apps.pictures.middlewares.AutoLogoutMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

#HEROKU
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'd27qtj21sfr1b0',
#         'USER': 'uekvi0ou38jfmr',
#         'PASSWORD': 'p473912e85023c0677a816c0e3f3bc8d3b1e07fc01eed9d5d2d76b4b919598e4f',
#         'HOST': 'c3nv2ev86aje4j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com',
#         'PORT': 5432,
#         'CONN_MAX_AGE': 600,
#         'OPTIONS': {
#             'connect_timeout': 60,
#         },
#     }
# }


#AWS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'spotlightdatabase',
        'USER': 'manager',
        'PASSWORD': 'l4TJsvRQD6wOWjCr1grd',
        'HOST': 'spotlightdatabase.cj0qe448e9p0.us-west-1.rds.amazonaws.com',
        'PORT': 5432,
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 60,
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# AWS S3 configuration for storing static, media, and converted images files
AWS_STORAGE_BUCKET_NAME =os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID =os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY =os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME =os.getenv('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_S3_FILE_OVERWRITE = False

AWS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
}

AWS_QUERYSTRING_AUTH = False

USE_S3 = True 
# Custom storage backends for static and media files
S3_ACCELERATE_ENDPOINT = 'spotlight-prod-us-west-1-static-media.s3-accelerate.amazonaws.com'
# Static files (CSS, JavaScript, Images)
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "setup/static")
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (uploaded files)
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Converted images storage
CONVERTED_IMAGES_DIR = os.path.join(settings.MEDIA_ROOT, 'converted_images')
CONVERTED_IMAGES_URL = f'{settings.MEDIA_URL}converted_images/'
os.makedirs(CONVERTED_IMAGES_DIR, exist_ok=True)

#Authentication
LOGIN_REDIRECT_URL = 'userOrders--page'
LOGOUT_REDIRECT_URL = 'logout'
LOGIN_URL = 'login'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

DATA_UPLOAD_MAX_NUMBER_FILES = 10000 # or any number you need

DATA_UPLOAD_MAX_MEMORY_SIZE = 500 * 1024 * 1024 * 1024  # 500 GB
FILE_UPLOAD_MAX_MEMORY_SIZE = 500 * 1024 * 1024 * 1024  # 500 GB


AUTH_USER_MODEL = 'users.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', 
    'apps.users.authentication.EmailOrUsernameModelBackend',  
]

AUTO_LOGOUT_DELAY = 1800

SESSION_COOKIE_AGE = 1800  # 30 min

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_SAVE_EVERY_REQUEST = True
