# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-11 15:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20171211_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_rating', models.CharField(choices=[('1', 'very bad'), ('2', 'bad'), ('3', 'medium'), ('4', 'good'), ('5', 'over 9000')], max_length=512)),
                ('rating', models.CharField(max_length=512)),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Trainer')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.RegUser')),
            ],
        ),
    ]
