import os
from pathlib import Path
from fincrest.utils.keyvault import get_secret

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_secret("DJANGO-SECRET-KEY")  # 👈 Fetch directly from Key Vault

if not SECRET_KEY:
    raise ValueError("❌ SECRET_KEY is missing. Make sure it's stored in Key Vault and accessible.")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "fincrest-backend.azurewebsites.net").split(",")

# ✅ Database settings from Azure Key Vault
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("DB-NAME"),
        "USER": os.getenv("DB-USER"),
        "PASSWORD": os.getenv("DB-PASSWORD"),
        "HOST": os.getenv("DB-HOST"),
        "PORT": "5432",
    }
}

if not DATABASES["default"]["NAME"]:
    raise ValueError("❌ DATABASE NAME (DB-NAME) is not set! Check Azure environment variables.")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "fincrest",  
    "apps.ai_engine",
    "apps.azure_integration",
    "apps.data_connectors",
    "apps.financial_core",
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

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  
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

# ✅ Static Files for Azure
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ✅ Logging for Azure
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django-error.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
