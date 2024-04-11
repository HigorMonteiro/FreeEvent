from __future__ import annotations

import dj_database_url
from decouple import config
from split_settings.tools import include


include(
    'base.py',
    'application.py',
    'auth.py',
    'security.py',
    'storage.py',
    'rest.py',
    'spectacular.py',
)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DB_URL = 'sqlite:///db.sqlite3'

CONN_MAX_AGE = int(config('CONN_MAX_AGE', default='600'))
DATABASES = {
    'default': dj_database_url.parse(DB_URL, conn_max_age=CONN_MAX_AGE),
}
