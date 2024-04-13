import logging

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from api.account.models import User
from api.common.model import CoreModel
from api.common.utils import EventStatus
from api.tasks.app import notify_participants_async


logger = logging.getLogger('api.core.models')


class Address(CoreModel):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.street


class Participant(User, CoreModel):
    phone = models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        db_table = 'participants'
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'

    def save(self, *args, **kwargs):
        self.is_active = True
        self.is_staff = False
        if not self.password:
            random_password = get_random_string(length=8)
            self.password = random_password
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Event(CoreModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Participant, related_name='events', blank=True)
    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in EventStatus],
        default=EventStatus.DRAFT.name,
    )

    class Meta:
        db_table = 'events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Event)
def send_notification_if_changed(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_event = Event.objects.get(pk=instance.pk)
            if old_event.status == EventStatus.CANCELED.name:
                return
            if (
                instance.date != old_event.date
                or instance.time != old_event.time
            ):
                notify_participants_async.delay(
                    str(instance.id),
                    instance.date,
                    instance.time,
                    str(instance.address),
                )
            if instance.status == EventStatus.CANCELED.name:
                notify_participants_async.delay(str(instance.id))
            logger.info('Notification sent to participants')
        except Event.DoesNotExist:
            pass


@receiver(pre_save, sender=Participant)
def send_welcome_email(sender, instance, **kwargs):
    print('INSTANCE', instance)
    if instance.pk:
        try:
            old_participant = Participant.objects.get(pk=instance.pk)
            if not old_participant.is_active and instance.is_active:
                notify_participants_async.delay(str(instance.random_password), instance.email)
                logger.info('Welcome email sent to participant')
        except Participant.DoesNotExist:
            pass
