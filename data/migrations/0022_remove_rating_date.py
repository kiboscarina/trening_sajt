# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-15 20:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0021_auto_20171214_1225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='date',
        ),
    ]
