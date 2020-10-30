# Generated by Django 3.0.6 on 2020-10-20 12:40

from django.db import migrations, models
import netfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web_net', '0017_vlan_trash_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='VPN',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pull', netfields.fields.InetAddressField(max_length=39, unique=True, verbose_name='Пул')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'VPN pool',
                'ordering': ('pull',),
            },
        ),
        migrations.DeleteModel(
            name='Tunnels',
        ),
    ]