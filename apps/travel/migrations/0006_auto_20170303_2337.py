# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 23:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg', '0001_initial'),
        ('travel', '0005_auto_20170303_2334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='planner',
        ),
        migrations.AddField(
            model_name='trip',
            name='planner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='trip_planner', to='login_reg.User'),
        ),
    ]
