# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0015_auto_20171213_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='average_value',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]