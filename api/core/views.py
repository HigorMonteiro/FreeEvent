import logging

from django.http import JsonResponse
from rest_framework import mixins, viewsets
from rest_framework.views import APIView

from api.common.routers import CustomViewRouter
from api.core.serializers import EventSerializer, ParticipantSerializer
from api.tasks.app import generate_csv_report

from .models import Event, Participant


router = CustomViewRouter()

logger = logging.getLogger(__name__)


@router.register('participants', basename='participant')
class ParticipantView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@router.register('events', basename='event')
class EventView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ExportEventAPI(APIView):

    def get(self, request, *args, **kwargs):
        task = generate_csv_report.delay()

        return JsonResponse({'task_id': task.id}, status=202)
