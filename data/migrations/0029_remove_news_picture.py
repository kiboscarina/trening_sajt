# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-04-24 09:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0028_auto_20190319_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='picture',
        ),
    ]
