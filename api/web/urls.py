from __future__ import annotations

import logging

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from drf_spectacular import views
from drf_spectacular.utils import extend_schema


logger = logging.getLogger(__name__)

_swagger_urlpatterns = [
    path(
        'api/v1/schema/',
        extend_schema(exclude=True)(views.SpectacularAPIView).as_view(),
        name='schema',
    ),
    path(
        'docs/',
        extend_schema(exclude=True)(views.SpectacularSwaggerView).as_view(
            url_name='schema',
        ),
        name='swagger-ui',
    ),
    path(
        'redoc/',
        extend_schema(exclude=True)(views.SpectacularRedocView).as_view(
            url_name='schema',
        ),
        name='redoc',
    ),
]

urlpatterns = [
    *_swagger_urlpatterns,
    path('', lambda _request: redirect('docs/'), name='home'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT,
)

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
)
