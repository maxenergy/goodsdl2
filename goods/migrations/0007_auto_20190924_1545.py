# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-09-24 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_auto_20190923_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelfimage',
            name='shelfid',
            field=models.CharField(db_index=True, default=0, max_length=100),
        ),
    ]
