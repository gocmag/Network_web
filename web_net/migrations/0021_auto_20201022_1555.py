# Generated by Django 3.0.6 on 2020-10-22 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_net', '0020_auto_20201022_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adress',
            name='ip_address',
            field=models.GenericIPAddressField(),
        ),
    ]