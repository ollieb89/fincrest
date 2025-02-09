import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from Azure App Service (no .env file required)
SECRET_KEY = os.getenv("SECRET_KEY")
BINANCE_WS_URL = os.getenv("BINANCE_WS_URL")
BINANCE_WS_USER = os.getenv("BINANCE_WS_USER")
AZURE_VAULT_URL = os.getenv("AZURE_VAULT_URL")

# Ensure required variables are set
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set! Make sure it's configured in Azure.")

if not AZURE_VAULT_URL:
    raise ValueError("AZURE_VAULT_URL is missing. Add it in Azure settings.")

ROOT_URLCONF = "fincrest.urls"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
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

# 👇 Add this TEMPLATES setting:
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # 👈 Directory for custom templates
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
