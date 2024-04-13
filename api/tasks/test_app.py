from io import StringIO
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.test import override_settings
from model_bakery import baker

from api.core.models import EventStatus
from api.tasks.app import generate_csv_report, notify_participants_async


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


@pytest.mark.django_db
def test_generate_csv_report(tmpdir):

    participants_01 = [
        baker.make('Participant', email='email01'),
        baker.make('Participant', email='email03'),
    ]
    participants_02 = [
        baker.make('Participant', email='email02'),
        baker.make('Participant', email='email04'),
    ]

    baker.make('Event', title='Event 1', participants=participants_01)
    baker.make('Event', title='Event 2', participants=participants_02)

    with patch('builtins.open', create=True) as mock_open:
        mock_file = mock_open.return_value
        mock_file.write.side_effect = StringIO().write

        result = generate_csv_report()
        mock_open.assert_called_once_with('report.csv', 'w', encoding='utf-8')
    assert result == 'report.csv'
