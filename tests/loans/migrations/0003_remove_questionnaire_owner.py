# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 08:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0002_auto_20171119_2008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaire',
            name='owner',
        ),
    ]