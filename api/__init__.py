from __future__ import annotations
from django.apps import apps

import os

__version__ = "0.1.0"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.config.settings")

if not apps.ready:
    import django
    django.setup()