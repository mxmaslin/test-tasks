# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 09:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu_tag', '0003_auto_20171126_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='menu_tag.Menu'),
        ),
    ]