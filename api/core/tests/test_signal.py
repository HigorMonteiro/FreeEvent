from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from api.core.models import Event, EventStatus, send_notification_if_changed


User = get_user_model()


@pytest.mark.django_db
class EventSignalTests(TestCase):
    def setUp(self):
        self.participants = baker.make(
            'core.Participant', make_m2m=True, _quantity=100,
        )
        self.address = baker.make('core.Address')
        self.event = baker.make(
            'core.Event',
            participants=self.participants,
            date=timezone.now().date(),
            time=timezone.now().time(),
            address=self.address,
            status=EventStatus.PUBLISHED.name,
        )

        self.event_canceled = baker.make(
            'core.Event',
            participants=self.participants,
            date=timezone.now().date(),
            time=timezone.now().time(),
            address=self.address,
            status=EventStatus.CANCELED.name,
        )

    def test_send_notification_if_changed(self):
        self.event.date = timezone.now().date() + timezone.timedelta(days=1)
        self.event.save()

        with self.assertLogs('api.core.models', level='INFO') as cm:
            send_notification_if_changed(sender=Event, instance=self.event)

        self.assertEqual(len(cm.records), 1)
        self.assertEqual(cm.records[0].levelname, 'INFO')
        self.assertEqual(
            cm.records[0].message, 'Notification sent to participants',
        )

        self.event.status = EventStatus.CANCELED.name
        self.event.save()

    def test_send_notification_if_changed_canceled(self):
        with patch(
            'api.core.models.send_notification_if_changed',
        ) as mock_task:
            self.event_canceled.save()

            mock_task.assert_not_called()
