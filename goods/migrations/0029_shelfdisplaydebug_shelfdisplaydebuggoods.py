# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-11-21 18:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0028_auto_20191121_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShelfDisplayDebug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tz_id', models.IntegerField()),
                ('display_source', models.CharField(default='', max_length=200)),
                ('category_intimacy_source', models.CharField(default='', max_length=200)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date created')),
            ],
        ),
        migrations.CreateModel(
            name='ShelfDisplayDebugGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
                ('goods_tree_source', models.CharField(default='', max_length=200)),
                ('shelf_display_debug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shelf_display_debug_goods', to='goods.ShelfImage2')),
            ],
        ),
    ]