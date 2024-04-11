import uuid
from enum import Enum

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.account.models import User
from api.tasks.app import notify_participants_async


class CoreModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class EventStatus(Enum):
    DRAFT = 'rascunho'
    PUBLISHED = 'publicado'
    FILED = 'arquivado'
    CANCELED = 'cancelado'
    CONCLUDED = 'finalizado'


class Event(CoreModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Participant, related_name='events')
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


@receiver(post_save, sender=Event)
def trigger_notify_participants(sender, instance, **kwargs):
    notify_participants_async.delay(str(instance.id))
