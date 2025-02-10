from fincrest.utils.keyvault import get_secret

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fincrest',  # ✅ Make sure this is here
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('DB-NAME'),
        'USER': get_secret('DB-USER'),
        'PASSWORD': get_secret('DB-PASSWORD'),
        'HOST': get_secret('DB-HOST'),
        'PORT': '5432',
    }
}

SECRET_KEY = get_secret('DJANGO-SECRET-KEY')

ALLOWED_HOSTS = ["fincrest-backend.azurewebsites.net"]