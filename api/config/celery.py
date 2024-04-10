from __future__ import annotations

from decouple import config

from api.config.application import TIME_ZONE


broker_url = config('CELERY_BROKER_URL', 'redis://localhost:6379/0')
result_backend = config('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

task_always_eager = config('CELERY_TASK_ALWAYS_EAGER', 'False')
task_eager_propagates = config('CELERY_TASK_EAGER_PROPAGATES', 'False')
task_ignore_result = config('CELERY_TASK_IGNORE_RESULT', 'False')

timezone = TIME_ZONE
enable_utc = True
