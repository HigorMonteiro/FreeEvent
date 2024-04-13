# Generated by Django 5.0.4 on 2024-04-13 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_alter_event_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="participants",
            field=models.ManyToManyField(
                blank=True, related_name="events", to="core.participant"
            ),
        ),
    ]
