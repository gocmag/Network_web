# Generated by Django 3.0.6 on 2020-08-19 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_net', '0013_region_geokod'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ('geokod',), 'verbose_name': 'Region'},
        ),
    ]