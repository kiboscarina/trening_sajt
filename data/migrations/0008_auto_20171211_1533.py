# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-11 15:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='trainer',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]