# Generated by Django 3.0.6 on 2020-05-25 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_net', '0002_adress'),
    ]

    operations = [
        migrations.AddField(
            model_name='adress',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
