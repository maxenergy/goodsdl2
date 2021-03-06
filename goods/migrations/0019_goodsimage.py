# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-10-31 15:12
from __future__ import unicode_literals

from django.db import migrations, models
import goods.models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0018_auto_20191023_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rgb_source', models.ImageField(max_length=200, upload_to=goods.models.goods_image_upload_source)),
                ('depth_source', models.ImageField(max_length=200, upload_to=goods.models.goods_image_upload_source)),
                ('table_z', models.IntegerField(default=0)),
                ('result', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date created')),
            ],
        ),
    ]
