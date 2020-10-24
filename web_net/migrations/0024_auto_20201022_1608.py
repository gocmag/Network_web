# Generated by Django 3.0.6 on 2020-10-22 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_net', '0023_remove_adress_vpnpool_reletionship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adress',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='adress',
            name='ip_address',
            field=models.GenericIPAddressField(unique=True),
        ),
        migrations.AlterField(
            model_name='adress',
            name='network_reletionship',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web_net.Networks'),
        ),
    ]
