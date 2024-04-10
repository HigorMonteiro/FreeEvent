from __future__ import annotations

import logging
from typing import Any, cast

from decouple import config
from storages.backends.s3 import S3Storage

from api.config.base import BASE_DIR


logger = logging.getLogger(__name__)

USE_S3_FOR_MEDIA = config('USE_S3_FOR_MEDIA', default='False')
USE_S3_FOR_STATIC = config('USE_S3_FOR_STATIC', default='False')

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STORAGES = {
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'
if config('AWS_STORAGE_BUCKET_NAME', default=None):
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', 'bucket')
    AWS_S3_CUSTOM_DOMAIN = config(
        'AWS_S3_CUSTOM_DOMAIN',
        f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com',
    )
    AWS_S3_ENDPOINT_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}'

    AWS_S3_ACCESS_KEY_ID = config('AWS_S3_ACCESS_KEY_ID', 'access_key')
    AWS_S3_SECRET_ACCESS_KEY = config('AWS_S3_SECRET_ACCESS_KEY', 'secret_key')

    AWS_S3_CONFIG = {
        'BACKEND': 'api.config.storage.CustomDomainS3Storage',
        'OPTIONS': {
            'bucket_name': AWS_STORAGE_BUCKET_NAME,
            'access_key': AWS_S3_ACCESS_KEY_ID,
            'secret_key': AWS_S3_SECRET_ACCESS_KEY,
            'endpoint_url': AWS_S3_ENDPOINT_URL,
        },
    }

    STORAGES: dict[str, Any] = {}

    if USE_S3_FOR_STATIC:
        logger.info('Serving static files from S3')
        STORAGES['staticfiles'] = AWS_S3_CONFIG
    else:
        logger.info('Serving static files locally')
        STORAGES['staticfiles'] = {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        }

    if USE_S3_FOR_MEDIA:
        logger.info('Serving media files from S3')
        STORAGES['default'] = AWS_S3_CONFIG
    else:
        logger.info('Serving media files locally')
        STORAGES['default'] = {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
            'LOCATION': MEDIA_ROOT.as_posix(),
            'BASE_URL': MEDIA_URL,
        }


class CustomDomainS3Storage(S3Storage):
    """Extend S3 with signed URLs for custom domains."""

    custom_domain = False

    def url(
        self,
        name: str,
        parameters: Any = None,
        expire: Any = None,
        http_method: Any = None,
    ) -> str:
        """Replace internal domain with custom domain for signed URLs."""
        url = cast(str, super().url(name, parameters, expire, http_method))

        return url.replace(
            f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com',
            AWS_S3_ENDPOINT_URL,
        )
