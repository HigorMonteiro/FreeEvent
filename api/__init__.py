from __future__ import annotations

import os

import django


__version__ = '0.1.0'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.config.settings')
django.setup()
