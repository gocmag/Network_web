# Generated by Django 3.0.6 on 2020-12-01 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_net', '0004_auto_20201201_1908'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testdb',
            options={'ordering': ('network_binary',)},
        ),
        migrations.AlterField(
            model_name='testdb',
            name='network_binary',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
