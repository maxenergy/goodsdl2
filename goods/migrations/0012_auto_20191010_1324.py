# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-10-10 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0011_shelfgoods_is_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelfgoods',
            name='col',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='shelfgoods',
            name='process_code',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='shelfgoods',
            name='row',
            field=models.IntegerField(default=-1),
        ),
    ]
