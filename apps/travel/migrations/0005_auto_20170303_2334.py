# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 23:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0004_auto_20170303_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='traveler',
            field=models.ManyToManyField(default=3, related_name='travel_user', to='login_reg.User'),
        ),
    ]
