# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-11-26 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0031_auto_20191126_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='allworkflowbatch',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='date updated'),
        ),
        migrations.AlterField(
            model_name='allworkflowbatch',
            name='auto_display_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='allworkflowbatch',
            name='batch_id',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='allworkflowbatch',
            name='order_goods_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='allworkflowbatch',
            name='select_goods_status',
            field=models.IntegerField(default=1),
        ),
    ]
