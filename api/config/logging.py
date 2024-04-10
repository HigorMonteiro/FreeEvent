from __future__ import annotations

import logging.config


LOG_LEVEL = 'INFO'
FORMAT = '%(asctime)s %(log_color)s%(levelname)s %(name)s %(message)s'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}

logging.config.dictConfig(LOGGING)
