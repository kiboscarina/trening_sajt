# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-16 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0023_remove_rating_average_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer',
            name='average_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]
