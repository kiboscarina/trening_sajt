# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-03-19 11:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0026_auto_20190319_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reguser',
            name='profilePicture',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='users_pic'),
        ),
    ]