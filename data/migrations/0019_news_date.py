# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 10:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0018_auto_20171214_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
