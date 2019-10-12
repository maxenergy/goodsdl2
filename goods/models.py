from django.db import models
import datetime
from django.conf import settings

class ShelfImage(models.Model):
    picid = models.IntegerField(default=0, db_index=True)
    shopid = models.IntegerField(default=0, db_index=True)
    shelfid = models.CharField(default='', max_length=100, db_index=True)
    displayid = models.IntegerField(default=0)
    tlevel = models.IntegerField(default=0)
    picurl = models.CharField(max_length=200, default='')
    source = models.CharField(max_length=200, default='')
    rectjson = models.TextField(default='')
    rectsource = models.CharField(max_length=200, default='')
    score = models.IntegerField(default=0)
    equal_cnt = models.IntegerField(default=0)
    different_cnt = models.IntegerField(default=0)
    unknown_cnt = models.IntegerField(default=0)
    resultsource = models.CharField(max_length=200, default='')
    test_server = models.BooleanField(default=True)
    create_time = models.DateTimeField('date created', auto_now_add=True)
    update_time = models.DateTimeField('date updated', auto_now=True)

class ShelfGoods(models.Model):
    shelf_image = models.ForeignKey(ShelfImage, related_name="shelf_image_goods", on_delete=models.CASCADE)
    upc = models.CharField(max_length=20,default='')
    xmin = models.PositiveIntegerField(default=0)
    ymin = models.PositiveIntegerField(default=0)
    xmax = models.PositiveIntegerField(default=0)
    ymax = models.PositiveIntegerField(default=0)
    level = models.IntegerField(default=-1)
    result = models.IntegerField(default=-1)
    is_label = models.BooleanField(default=False)
    process_code = models.IntegerField(default=-1)
    col = models.IntegerField(default=-1)
    row = models.IntegerField(default=-1)
    baidu_code = models.CharField(max_length=50,default='')
    create_time = models.DateTimeField('date created', auto_now_add=True,db_index=True)
    update_time = models.DateTimeField('date updated', auto_now=True)
    def __str__(self):
        return '{}-{}:{}'.format(self.pk, self.upc, self.result)

def image_upload_source(instance, filename):
    now = datetime.datetime.now()
    return '{}/{}/{}/{}/{}_{}_{}'.format(settings.DETECT_DIR_NAME, 'freezer', now.strftime('%Y%m'),
                                         now.strftime('%d%H'), now.strftime('%M%S'), str(now.time()), filename)


class FreezerImage(models.Model):
    deviceid = models.CharField(max_length=20, default='0', db_index=True)
    ret = models.TextField(default='')
    source = models.ImageField(max_length=200, upload_to=image_upload_source)
    visual = models.URLField(max_length=200, default='')
    create_time = models.DateTimeField('date created', auto_now_add=True, db_index=True)

