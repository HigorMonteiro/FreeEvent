from __future__ import annotations

from celery import Celery, shared_task
from django.core.mail import EmailMessage

from api.config import celery as config


app = Celery('api.config')
app.config_from_object(config)
app.autodiscover_tasks()


@shared_task
def notify_participants_async(
    event_id, event_status=None, date=None, address=None,
):
    from api.core.models import Event

    event = Event.objects.get(id=event_id)

    header = 'Evento Atualizado'

    message = 'O evento em que você está participando foi atualizado.\n'
    if event_status:
        message += f'Status: {event.status}\n'
    if date:
        message += f'Nova Data: {event.date}\n'
    if address:
        message += f'Localização: {event.address}\n'

    email = EmailMessage(
        header,
        message,
        'contato@free-event.com.br',
        [p.email for p in event.participants.all()],
    )
    email.send()
