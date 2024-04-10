from __future__ import annotations

import logging

from decouple import config
from django.core.cache import cache
from redis.exceptions import RedisError


logger = logging.getLogger(__name__)

USE_REDIS_FOR_CACHE = config('USE_REDIS_FOR_CACHE', default='True')
REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')

CACHES = {}

if USE_REDIS_FOR_CACHE:
    logger.info('Using Redis for cache')
    CACHES['default'] = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }

    # Ping the cache to see if it's working
    try:
        cache.set('ping', 'pong')

        if cache.get('ping') != 'pong':
            msg = 'Cache is not working properly.'
            raise ValueError(msg)  # noqa: TRY301

        cache.delete('ping')

        logger.info('Cache is working properly')
    except (ValueError, RedisError):
        logger.exception('Cache is not working. Using dummy cache instead')
        CACHES['default'] = {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
else:
    logger.warning('Using dummy cache')
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
