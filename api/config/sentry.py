from __future__ import annotations

import logging

from decouple import config
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from api.config.application import ENVIRONMENT

logger = logging.getLogger(__name__)

USE_SENTRY = config("USE_SENTRY", default="false").lower() == "true"

if USE_SENTRY:
    import sentry_sdk

    DSN = config("SENTRY_DSN")
    TRACES_SAMPLE_RATE = float(
        config("SENTRY_TRACES_SAMPLE_RATE", default="1.0")
    )
    PROFILE_SAMPLE_RATE = float(
        config("SENTRY_PROFILE_SAMPLE_RATE", default="1.0"),
    )

    sentry_sdk.init(
        dsn=DSN,
        environment=ENVIRONMENT,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
        ],
        traces_sample_rate=TRACES_SAMPLE_RATE,
        profiles_sample_rate=PROFILE_SAMPLE_RATE,
        send_default_pii=True,
    )

    logger.info("Sentry is initialized")
else:
    logger.info("Sentry is not initialized")
