# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-16 14:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0022_remove_rating_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='average_value',
        ),
    ]
