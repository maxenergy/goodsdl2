from django.db import models
import datetime
from django.conf import settings

class ShelfImage(models.Model):
    shopid = models.IntegerField(default=0, db_index=True)
    shelfid = models.IntegerField(default=0, db_index=True)
    picurl = models.CharField(max_length=200, default='0')
    image_name = models.CharField(max_length=200, default='')
    create_time = models.DateTimeField('date created', auto_now_add=True)

class ShelfGoods(models.Model):
    shelf_image = models.ForeignKey(ShelfImage, related_name="shelf_image_goods", on_delete=models.CASCADE)
    shopid = models.IntegerField(default=0, db_index=True)
    shelfid = models.IntegerField(default=0, db_index=True)
    score1 = models.FloatField(default=0.0)
    score2 = models.FloatField(default=0.0)
    upc = models.CharField(max_length=20)
    xmin = models.PositiveIntegerField(default=0)
    ymin = models.PositiveIntegerField(default=0)
    xmax = models.PositiveIntegerField(default=0)
    ymax = models.PositiveIntegerField(default=0)
    level = models.IntegerField(default=-1)
    create_time = models.DateTimeField('date created', auto_now_add=True,db_index=True)
    update_time = models.DateTimeField('date updated', auto_now=True)
