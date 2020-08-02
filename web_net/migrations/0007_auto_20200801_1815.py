# Generated by Django 3.0.6 on 2020-08-01 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_net', '0006_auto_20200801_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='BO',
            fields=[
                ('geokod', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='tunnels',
            name='firstTunnelDevice',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tunnels',
            name='secondTunnelDevice',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
