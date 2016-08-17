# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-16 21:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('traveldashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='trip',
            managers=[
                ('tripManager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='attending',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='TripToAttending', to='traveldashboard.User'),
        ),
        migrations.AddField(
            model_name='trip',
            name='created_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='TripToCreator', to='traveldashboard.User'),
        ),
    ]