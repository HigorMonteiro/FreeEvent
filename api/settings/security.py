from __future__ import annotations

import logging

from decouple import config

logger = logging.getLogger(__name__)

SECRET_KEY = config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG")

ALLOWED_HOSTS = [
    host.strip()
    for host in config("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

CSRF_TRUSTED_ORIGINS = [
    host.strip()
    for host in config("CSRF_TRUSTED_ORIGINS", "http://localhost").split(",")
]

CORS_ALLOW_ALL_ORIGINS = bool(config("CORS_ALLOW_ALL_ORIGINS", "False"))
CORS_ALLOW_CREDENTIALS = bool(config("CORS_ALLOW_CREDENTIALS", "False"))
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS", "http://localhost"
).split(",")
