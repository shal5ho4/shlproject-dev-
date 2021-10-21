from pathlib import Path
from environs import Env
import os


env = Env()
env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = ['shldepot.com', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'listings.apps.ListingsConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'django_extensions',
    'social_django',
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

ROOT_URLCONF = 'shl_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(os.path.join(BASE_DIR, 'templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shl_project.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'shl_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DATABASE_NAME'),
        'USER': env.str('DATABASE_USER'),
        'PASSWORD': env.str('DATABASE_PASSWORD'),
        'HOST': 'localhost'
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

LOGIN_URL = 'login'

LOGOUT_REDIRECT_URL = 'listings:product_list'


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (str(os.path.join(BASE_DIR, 'static')),)

STATIC_ROOT = str(os.path.join(BASE_DIR, 'staticfiles/'))

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# Cart session

CART_ID = 'cart'


# Stripe API keys

STRIPE_TEST_PUBLISHABLE_KEY = env.str('STRIPE_TEST_PUB')

STRIPE_TEST_SECRET_KEY = env.str('STRIPE_TEST_SEC')


# Email config

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = 'sharuru.test@gmail.com'

EMAIL_HOST = 'smtp.sendgrid.net'

EMAIL_HOST_USER = 'apikey'

EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')

EMAIL_PORT = 587

EMAIL_USE_TLS = True


# social_auth config

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.google.GoogleOAuth2',
]

SOCIAL_AUTH_TWITTER_KEY = env.str('TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = env.str('TWITTER_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env.str('GOOGLE_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env.str('GOOGLE_SECRET')


# Redis config

REDIS_HOST = 'localhost'

REDIS_PORT = 6379

REDIS_DB = 1
