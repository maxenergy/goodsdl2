
import time
from goods.sellgoods.salesquantity.service.order_version_5 import order_process
from django.db import close_old_connections
def generate_data():
    print ("生成自动订单数据")
    while True:
        time.sleep(5)
        close_old_connections()
        try:
            order_process.first_order_process()
        except Exception as e:
            print ("order_process.first_order_process  error e={}".format(e))

        try:
            order_process.day_order_process()
        except Exception as e:
            print("order_process.day_order_process  error e={}".format(e))

        try:
            order_process.add_order_process()
        except Exception as e:
            print("order_process.add_order_process  error e={}".format(e))
if __name__=='__main__':
    generate_data()