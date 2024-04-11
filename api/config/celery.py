from __future__ import annotations

from decouple import config

from api.config.application import TIME_ZONE


broker_url = config('CELERY_BROKER_URL')
result_backend = config('CELERY_RESULT_BACKEND')

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

timezone = TIME_ZONE
enable_utc = True
