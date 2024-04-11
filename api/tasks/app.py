from __future__ import annotations

import time

from celery import Celery, shared_task
from django.core.mail import send_mail

from api.config import celery as config


app = Celery('api.config')
app.config_from_object(config)
app.autodiscover_tasks()


@shared_task
def notify_participants_async(event_id):
    from api.core.models import Event  # Import here to avoid circular import

    time.sleep(10)
    event = Event.objects.get(id=event_id)
    send_mail(
        f'Event Updated -> {event.title}',
        'The event you are participating in has been updated.',
        'from@example.com',
        [p.email for p in event.participants.all()],
        fail_silently=False,
    )
