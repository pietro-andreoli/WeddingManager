# Generated by Django 3.1.7 on 2021-04-25 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvitationManager', '0008_auto_20210417_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='email',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='phone_number',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
