from __future__ import annotations

import logging

import dj_database_url
from decouple import config


logger = logging.getLogger(__name__)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

_default_db_url = 'sqlite:///db.sqlite3'
DB_URL = config('DATABASE_URL', default=_default_db_url)

if _default_db_url == DB_URL:
    logger.warning("Using default database url: '%s'", DB_URL)

CONN_MAX_AGE = int(config('CONN_MAX_AGE', default='600'))
DATABASES = {
    'default': dj_database_url.parse(DB_URL, conn_max_age=CONN_MAX_AGE),
}
