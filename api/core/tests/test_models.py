import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker

from api.core.models import EventStatus


User = get_user_model()


@pytest.mark.django_db
def test_event_creation():
    title = 'Test Event'
    description = 'This is a test event'
    date = '2022-01-01'
    time = '12:00:00'
    participants = baker.make('core.Participant', make_m2m=True, _quantity=100)
    address = baker.make('core.Address')
    status = EventStatus.DRAFT.name

    event = baker.make(
        'core.Event',
        title=title,
        description=description,
        date=date,
        time=time,
        address=address,
        participants=participants,
        status=status,
    )

    assert event.title == title
    assert event.description == description
    assert event.address == address
    assert event.participants.count() == 100
    assert event.status == status
    assert str(event) == title


@pytest.mark.django_db
def test_event_status_choices():
    assert EventStatus.DRAFT.name == 'DRAFT'
    assert EventStatus.PUBLISHED.name == 'PUBLISHED'
    assert EventStatus.FILED.name == 'FILED'
    assert EventStatus.CANCELED.name == 'CANCELED'
    assert EventStatus.CONCLUDED.name == 'CONCLUDED'
    assert EventStatus.DRAFT.value == 'rascunho'
    assert EventStatus.PUBLISHED.value == 'publicado'
    assert EventStatus.FILED.value == 'arquivado'
    assert EventStatus.CANCELED.value == 'cancelado'
    assert EventStatus.CONCLUDED.value == 'finalizado'


@pytest.mark.django_db
def test_update_event_status():
    event = baker.make('core.Event')
    assert event.status == EventStatus.DRAFT.name

    event.status = EventStatus.PUBLISHED.name
    event.save()

    assert event.status == EventStatus.PUBLISHED.name
    assert event.status == 'PUBLISHED'
    assert event.status != EventStatus.PUBLISHED.value
    assert event.status != 'publicado'


@pytest.mark.django_db
def test_event_participants():
    participant = baker.make('core.Participant', username='test')
    event = baker.make('core.Event', participants=[participant])

    assert event.participants.last() == participant
    assert event.participants.last().username == participant.username
