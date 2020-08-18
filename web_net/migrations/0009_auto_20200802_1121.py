# Generated by Django 3.0.6 on 2020-08-02 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_net', '0008_auto_20200801_1834'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pat',
            options={'ordering': ('geokod',)},
        ),
        migrations.AddField(
            model_name='region',
            name='core',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='region',
            name='other',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='region',
            name='pat',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]