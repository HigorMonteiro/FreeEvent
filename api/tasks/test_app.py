import pytest
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.test import override_settings
from model_bakery import baker

from api.core.models import EventStatus
from api.tasks.app import notify_participants_async


User = get_user_model()


@pytest.mark.django_db
@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
)
def test_notify_participants_async(mocker):
    address = baker.make('Address', street='123 Main St')
    participants = baker.make('Participant', _quantity=10)
    event = baker.make(
        'Event',
        status=EventStatus.CANCELED.value,
        date='2022-01-01',
        address=address,
        participants=participants,
    )

    mocker.patch.object(EmailMessage, 'send')
    notify_participants_async(
        event.id, event_status=True, date='2022-01-02', address=address,
    )
    EmailMessage.send.assert_called_once_with()
