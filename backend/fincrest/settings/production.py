from fincrest.utils.keyvault import get_secret

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