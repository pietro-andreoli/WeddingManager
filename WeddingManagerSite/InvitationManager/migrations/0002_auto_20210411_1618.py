# Generated by Django 3.1.7 on 2021-04-11 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvitationManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='email',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='guest',
            name='fb_link',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='guest',
            name='home_address',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='guest',
            name='is_attending',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='guest',
            name='is_overseas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='guest',
            name='phone_number',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='guest',
            name='whose_guest',
            field=models.CharField(max_length=8, null=True),
        ),
    ]
