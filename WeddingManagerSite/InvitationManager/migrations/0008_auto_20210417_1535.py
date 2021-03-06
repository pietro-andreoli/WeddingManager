# Generated by Django 3.1.7 on 2021-04-17 19:35

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('InvitationManager', '0007_auto_20210411_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='invitation_name',
            field=models.CharField(default='NO NAME SET', max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='primary_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvitationManager.guest'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='assoc_invitation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvitationManager.invitation'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='fb_link',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='home_address',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='whose_guest',
            field=models.CharField(choices=[('peter', "Peter's"), ('tea', "Teodora's")], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='assoc_email',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvitationManager.invitation_email'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='invitation_url_id',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='seen_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='send_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
