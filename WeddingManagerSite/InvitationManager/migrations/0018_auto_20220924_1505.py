# Generated by Django 3.2.15 on 2022-09-24 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvitationManager', '0017_auto_20220920_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='ceremony_location_addr',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='config',
            name='ceremony_location_name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='config',
            name='ceremony_timestamp',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='config',
            name='reception_location_addr',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='config',
            name='reception_location_name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='config',
            name='reception_timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
