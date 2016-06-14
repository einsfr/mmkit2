# Этот файл содержит пример локальных настроек для разработки. Его нужно переименовать в dev-local.py для использования
import os

base_dir = os.environ.get("BASE_DIR")

ALLOWED_HOSTS = []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%%da))01s7@q1&%+hz3f6fmz=4)vdydl_e-vn_a+z7jjawn*22'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mmkit',
        'USER': 'mmkit',
        'PASSWORD': 'mmkit',
        'HOST': '127.0.0.1',
    }
}
