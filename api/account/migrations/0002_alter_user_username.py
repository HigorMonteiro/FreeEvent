# Generated by Django 5.0.4 on 2024-04-10 17:39

import django.core.validators
import re
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                help_text="Um nome curto que será usado para identificá-lo",
                max_length=30,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^[\\w.@+-]+$"),
                        "Informe um nome de usuário válido. Este valor deve conter apenas letras, números e os caracteres: @/./+/-/_ .",
                        "invalid",
                    )
                ],
                verbose_name="Apelido / Usuário",
            ),
        ),
    ]