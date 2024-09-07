"""
Django settings for opg_distribucija project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d8z1s@4_wtsibks%jonibl@=&&swymz^xx(d0bs5v$hz3j%gyl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'korisnicki_racuni',
    'opg',
    'opg_ponuda',
    'e_trznica',
    'django.contrib.gis',
    'kupac',
    'narudzbe',
]
 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'opg_distribucija.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'korisnicki_racuni.context_processors.dohvati_opg',
                'korisnicki_racuni.context_processors.dohvati_google_api',
                'korisnicki_racuni.context_processors.dohvati_korisnicki_profil',
                'e_trznica.context_processors.dohvati_brojac_kosarice',
                'e_trznica.context_processors.dohvati_iznose_u_kosarici',
                'korisnicki_racuni.context_processors.dohvati_paypal_client_id',
            ],
        },
    },
]

WSGI_APPLICATION = 'opg_distribucija.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'OpgDistribucija_DB',
        'USER': 'postgres',
        'PASSWORD': 'IIPprojekt24',
        'HOST': 'localhost',
    }
}

AUTH_USER_MODEL = 'korisnicki_racuni.User'

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

LANGUAGE_CODE = 'hr-BA'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR /'static'
STATICFILES_DIRS = [
    'opg_distribucija/static'
]

# Media files 
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR /'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}


EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtpout.secureserver.net'
EMAIL_HOST_USER='aplikacija@opgdistribucija.email'
EMAIL_HOST_PASSWORD='IIPprojekt24'
#DEFAULT_FROM_EMAIL='aplikacija@opgdistribucija.email' 
#EMAIL_PORT=465
#EMAIL_USE_SSL=True 
#EMAIL_USE_TLS=False
DEFAULT_FROM_EMAIL='OPG Distribucija <aplikacija@opgdistribucija.email>'
EMAIL_HOST='smtp.office365.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False


GOOGLE_API_KEY = 'AIzaSyAOHgwMw4V7Yzq0VO0xQWVonGyF-eXOHYU'


os.environ['PATH'] = os.path.join(BASE_DIR, 'env\Lib\site-packages\osgeo') + ';' + os.environ['PATH']
os.environ['PROJ_LIB'] = os.path.join(BASE_DIR, 'env\Lib\site-packages\osgeo\data\proj') + ';' + os.environ['PATH']
GDAL_LIBRARY_PATH = os.path.join(BASE_DIR, 'env\Lib\site-packages\osgeo\gdal.dll')



PAYPAL_CLIENT_ID = 'ATGZbOvDOL6yq7uhaAv4VokN5puvxerVVp46fb0-tr2Pg0_gcr91NHMGsEJLPxIHW2bb5DTLL53oLlQY'

SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'