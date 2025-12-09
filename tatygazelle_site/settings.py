from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------
# ENVIRONMENT LOADING
# ---------------------------------------

# Load .env only locally
if os.environ.get("RAILWAY_ENV") != "production":
    try:
        from dotenv import load_dotenv
        load_dotenv(BASE_DIR / ".env")
    except:
        pass

# ---------------------------------------
# SECURITY + DEBUG
# ---------------------------------------

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key")

# DEBUG is True only if environment variable explicitly equals "True"
DEBUG = os.environ.get("DEBUG", "False") == "True"

# Railway domain is provided via variables
RAILWAY_HOST = os.environ.get("RAILWAY_HOST", "")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

# Add Railway host if present
if RAILWAY_HOST:
    ALLOWED_HOSTS.append(RAILWAY_HOST)

# Add custom domain
ALLOWED_HOSTS += [
    "tatygazelle.com",
    "www.tatygazelle.com",
]

# ---------------------------------------
# CSRF TRUSTED ORIGINS
# ---------------------------------------

CSRF_TRUSTED_ORIGINS = [
    "https://tatygazelle.com",
    "https://www.tatygazelle.com",
]

if RAILWAY_HOST:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_HOST}")

# ---------------------------------------
# INSTALLED APPS
# ---------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "cloudinary",
    "cloudinary_storage",

    "main",
]

# ---------------------------------------
# MIDDLEWARE
# ---------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Must be right after SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tatygazelle_site.urls"

# ---------------------------------------
# TEMPLATES
# ---------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "main" / "templates"],
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

WSGI_APPLICATION = "tatygazelle_site.wsgi.application"

# ---------------------------------------
# DATABASE (Railway Postgres)
# ---------------------------------------

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=False,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ---------------------------------------
# STATIC FILES (Railway + Whitenoise)
# ---------------------------------------

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "main" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# In Production → compressed manifest storage
# In Dev → simpler static handling
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
    if not DEBUG
    else "whitenoise.storage.StaticFilesStorage"
)

# ---------------------------------------
# CLOUDINARY STORAGE
# ---------------------------------------

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
