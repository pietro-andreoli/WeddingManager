# Generated by Django 3.1.7 on 2021-04-11 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InvitationManager', '0004_invitation_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='invitation_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvitationManager.invitation'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='email_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvitationManager.invitation_email'),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_label', models.CharField(max_length=64, primary_key=True, serialize=False, unique=True)),
                ('primary_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvitationManager.guest')),
            ],
        ),
        migrations.AddField(
            model_name='guest',
            name='group_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvitationManager.group'),
        ),
    ]
