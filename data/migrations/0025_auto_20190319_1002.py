# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-03-19 10:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0024_auto_20171216_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer',
            name='picture',
            field=models.FileField(blank=True, default='default.jpg', null=True, upload_to='users_pic'),
        ),
    ]