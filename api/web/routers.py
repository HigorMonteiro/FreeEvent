from __future__ import annotations

from dataclasses import dataclass, field
from typing import cast

from django.urls import URLResolver, path
from rest_framework.routers import SimpleRouter
from rest_framework.viewsets import GenericViewSet, ViewSet


@dataclass
class CustomViewRouter:
    """Router for APIView and ViewSet."""

    url_prefix: str = ""

    _drf_router: SimpleRouter = field(default_factory=SimpleRouter)
    _paths: list[URLResolver] = field(default_factory=list)

    def register(
        self,
        route,
        name,
        basename,
        as_view_kwargs=None,
        **kwargs,
    ):
        route = f"{self.url_prefix}{route}"

        def decorator(view):
            if issubclass(view, (ViewSet, GenericViewSet)):
                kwargs.setdefault("basename", basename or name)
                self._drf_router.register(route, view, **kwargs)
            else:
                kwargs.setdefault("name", name or basename)
                self._paths.append(
                    path(
                        route, view.as_view(**(as_view_kwargs or {})), **kwargs
                    ),
                )

            return cast(view)

        return decorator

    @property
    def urls(self):
        return cast(self._paths + self._drf_router.urls)
