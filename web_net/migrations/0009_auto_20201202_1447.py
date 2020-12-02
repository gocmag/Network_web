# Generated by Django 3.0.6 on 2020-12-02 12:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_net', '0008_auto_20201202_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testdb',
            name='network_binary',
            field=models.BigIntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(code='invalid network', message='Неверный формат сети', regex='^1$')]),
        ),
    ]