
import pymysql
import datetime
import os,django,time
from goods.sellgoods.auto_choose_goods.haolinju_template import start_choose_goods

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()
from django.db import connections

if __name__ == '__main__':
    # conn = pymysql.connect('10.19.68.63', 'gpu_rw', password='jyrMnQR1NdAKwgT4', database='goodsdl',charset="utf8", port=3306, use_unicode=True)
    # cursor = conn.cursor()
    cursor = connections['default'].cursor()
    select_sql = "select batch_id,uc_shopid from goods_allworkflowbatch where select_goods_status=1"
    update_sql_01 = "update goods_allworkflowbatch set select_goods_status=2"    #2是正在计算、3是计算结束
    update_sql_02 = "update goods_allworkflowbatch set select_goods_status=3 and select_goods_calculate_time=123"    #2是正在计算、3是计算结束
    while True:
        time.sleep(5)
        print("circulation")
        cursor.execute(select_sql)
        all_data = cursor.fetchall()
        if all_data:
            for data in all_data:
                cursor.execute(update_sql_01)   # 更新到“正在计算”
                print('正在计算')
                connections['default'].commit()
                start_time = time.time()
                time.sleep(5)
                # start_choose_goods(data[0],data[1])   #计算中
                cursor.execute(update_sql_02)  # 更新到“结束计算”和耗时多少
                connections['default'].commit()
