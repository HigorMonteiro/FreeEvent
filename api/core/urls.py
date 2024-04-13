from __future__ import annotations

from django.urls import path

from api.core.views import ExportEventAPI, router


urlpatterns = [
    *router.urls,
    path('export-csv/', ExportEventAPI.as_view(), name='event_export'),
]
