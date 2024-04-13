from __future__ import annotations

import csv

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


@shared_task
def generate_csv_report():

    from api.core.models import Event

    events = Event.objects.all()

    with open('report.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Evento', 'Participantes'])
        for event in events:
            writer.writerow(
                [
                    event.title,
                    ', '.join([p.email for p in event.participants.all()]),
                ],
            )
    return 'report.csv'
