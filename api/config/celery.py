from __future__ import annotations

from decouple import config

from api.config.application import TIME_ZONE


broker_url = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
result_backend = config(
    'CELERY_RESULT_BACKEND', default='redis://localhost:6379/0',
)

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

timezone = TIME_ZONE
enable_utc = True
