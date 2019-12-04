import os
import smtplib,pymysql
from email.mime.text import MIMEText
import numpy as np
from PIL import Image as PILImage
import json
import django
import os
import time
import datetime
from  decimal import Decimal

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
# django.setup()

import main.import_django_settings


import math
from django.db import connections



class SendEmail():
    """
    注意️：
    只支持163和qq，需要登录邮箱开启smtp服务
    passwd: 163的话是邮箱密码，qq的话是授权码
    """

    def __init__(self, mail_account, passwd, recv):
        """
        :param mail_account: 邮箱账号
        :param passwd: 163的话是邮箱密码，qq的话是授权码
        :param recv: 邮箱接收人地址，多个账号以逗号隔开

        """
        self.mail_account = mail_account
        self.passwd = passwd
        self.recv = recv
        # self.title = title
        # self.content = content
        self.mail_host = mail_account.split('@')[1].split('.')[0]

    def send_mail(self,title,content):
        """
        :param title: 邮件标题
        :param content: 邮件内容
        :return:
        """

        try:
            msg = MIMEText(content)  # 邮件内容
            msg['Subject'] = title  # 邮件主题
            msg['From'] = self.mail_account  # 发送者账号
            msg['To'] = self.recv  # 接收者账号列表
            smtp = None
            if self.mail_host == '163':
                smtp = smtplib.SMTP('smtp.163.com', port=25)  # 连接邮箱，传入邮箱地址，和端口号，smtp的端口号是25
            if self.mail_host == 'qq':
                smtp = smtplib.SMTP_SSL('smtp.qq.com', port=465)
            smtp.login(self.mail_account, self.passwd)  # 发送者的邮箱账号，密码
            smtp.sendmail(self.mail_account, self.recv, msg.as_string())
            # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
            smtp.quit()  # 发送完毕后退出smtp
            print('email send success.')
        except:
            print('email send error.')

def calculate_goods_up_datetime(uc_shopid):
    """
    基于台账的计算商品的上架时间
    :param uc_shopid:  台账系统的shopid
    :return:
    """
    conn = connections['ucenter']
    cursor = conn.cursor()
    conn_ai = connections['default']
    cursor_ai = conn_ai.cursor()
    # 当前的台账
    select_sql_02 = "select t.id, t.shelf_id, td.batch_no,td.display_shelf_info, td.display_goods_info from sf_shop_taizhang st, sf_taizhang t, sf_taizhang_display td where st.taizhang_id=t.id and td.taizhang_id=t.id and td.status=2 and td.approval_status=1 and st.shop_id = {}".format(uc_shopid)
    insert_sql = "insert into goods_up_shelf_datetime(upc,shopid,name,up_shelf_date,is_new_goods,taizhang_batch_no) values (%s,{},%s,%s,1,%s)"
    select_sql_03 = "select upc,taizhang_batch_no from goods_up_shelf_datetime where shopid={}"
    delete_sql = "delete from goods_up_shelf_datetime where shopid={} and upc in {}"

    cursor.execute(select_sql_02)
    all_data = cursor.fetchall()

    cursor_ai.execute(select_sql_03.format(uc_shopid))
    history_data = cursor_ai.fetchall()

    history_upc_dict = {}    # 键为upc，值批次号
    for data in history_data:
        history_upc_dict[data[0]] = data[1]



    # 1、遍历新的台账，如果某个商品在所有历史的商品里，则不做操作；如果没在，则插入
    insert_data_list = []
    update_data_list = []
    new_upc_list = []
    for data in all_data:
        for goods_info in json.loads(data[4]):
            for layer in goods_info['layerArray']:
                for goods in layer:
                    goods_upc = goods['goods_upc']
                    new_upc_list.append(goods_upc)
                    goods_name = goods['name']
                    goods_up_shelf_datetime = data[2].split('_')[1]
                    if not goods_upc in history_upc_dict:      # 如果不在历史里，则作为新的插入
                        insert_data_list.append((goods_upc,goods_name,goods_up_shelf_datetime,data[2]))
                    else:
                        if data[2] != history_upc_dict[goods_upc]:     # 如果批次不相等，则是新的台账，品也相同，所以is_new_goods置为0
                            cursor_ai.execute("update goods_up_shelf_datetime set is_new_goods=0 where shopid={} and upc='{}'".format(uc_shopid,goods_upc))

    print('insert_data_list:',insert_data_list)
    cursor_ai.executemany(insert_sql.format(uc_shopid), tuple(insert_data_list))
    conn_ai.commit()
    print("上架时间插入成功")
    # 2、遍历历史商品表，如果每个商品没在新的台账里，则说明是下架的品，则删除
    delete_data_list = []
    for upc in history_upc_dict:
        if not upc in new_upc_list:
            delete_data_list.append(upc)
    print('delete_data_list:',delete_data_list)
    if delete_data_list:
        cursor_ai.execute(delete_sql.format(uc_shopid,tuple(delete_data_list)))
        conn_ai.commit()
    print("下架商品删除成功")

def calculate_goods_up_datetime_first(uc_shopid):
    """
    基于台账的计算商品的上架时间
    :param uc_shopid:  台账系统的shopid
    :return:
    """
    conn = connections['ucenter']
    cursor = conn.cursor()
    conn_ai = connections['default']
    cursor_ai = conn_ai.cursor()
    # 已完成的台账
    select_sql_01 = "select t.id, t.shelf_id, td.batch_no,td.display_shelf_info, td.display_goods_info from sf_shop_taizhang st, sf_taizhang t, sf_taizhang_display td where st.taizhang_id=t.id and td.taizhang_id=t.id and td.status=3 and td.approval_status=1 and st.shop_id = {}".format(uc_shopid)
    insert_sql = "insert into goods_up_shelf_datetime(upc,shopid,name,up_shelf_date,taizhang_batch_no) values (%s,{},%s,%s,%s)"
    select_sql_03 = "select upc from goods_up_shelf_datetime where shopid={}"
    delete_sql = "delete from goods_up_shelf_datetime where shopid={} and upc in {}"

    cursor.execute(select_sql_01)
    all_data = cursor.fetchall()

    cursor_ai.execute(select_sql_03.format(uc_shopid))



    # 1、遍历新的台账，如果某个商品在所有历史的商品里，则不做操作；如果没在，则插入
    insert_data_list = []
    update_data_list = []
    new_upc_list = []
    for data in all_data:
        print(type(data[1]))
        if data[1] == 1088:
            if not data[2].startswith('1142_20191106'):
                continue
        if data[1] == 1096:
            if not data[2].startswith('1169_20191107'):
                continue
        if data[1] == 1100:
            if not data[2].startswith('1169_20191107'):
                continue
        for goods_info in json.loads(data[4]):
            for layer in goods_info['layerArray']:
                for goods in layer:
                    goods_upc = goods['goods_upc']
                    new_upc_list.append(goods_upc)
                    goods_name = goods['name']
                    goods_up_shelf_datetime = data[2].split('_')[1]
                    insert_data_list.append((goods_upc, goods_name, goods_up_shelf_datetime,data[2]))
    print('insert_data_list:', insert_data_list)
    cursor_ai.executemany(insert_sql.format(uc_shopid), tuple(insert_data_list))
    conn_ai.commit()
    print("上架时间插入成功")
    cursor_ai.execute("update goods_up_shelf_datetime set is_new_goods=0 where shopid={}".format(uc_shopid))

def select_psd_data(upc,shop_id,time_range):
    """
    计算某商品在模板店一定取数周期内的psd和psd金额
    :param upc:
    :param shop_id: 目标门店，根据此id去查询模板id
    :param time_range: 取数周期
    :return: psd,psd金额
    """
    template_dict = {1284:3598}  # 临时解决方案，先写死
    template_shop_id = template_dict[shop_id]

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d %H:%M:%S')
    week_ago = (now - datetime.timedelta(days=time_range)).strftime('%Y-%m-%d %H:%M:%S')
    sql = "select sum(p.amount),g.upc,g.corp_classify_code,g.neighbor_goods_id,g.price,p.name from dmstore.payment_detail as p left join dmstore.goods as g on p.goods_id=g.id where p.create_time > '{}' and p.create_time < '{}' and p.shop_id={} and g.upc='{}';"
    # conn = pymysql.connect('123.103.16.19', 'readonly', password='fxiSHEhui2018@)@)', database='dmstore',charset="utf8", port=3300, use_unicode=True)
    conn = connections['dmstore']
    cursor = conn.cursor()
    cursor.execute(sql.format(week_ago,now_date,template_shop_id,upc))
    result = cursor.fetchone()
    cursor.close()
    # conn.close()
    if result:
        try:
            # print(result)
            return result[0]/(result[4]*time_range),result[0]/time_range
        except:
            # print("psd计算异常")
            return None,None
    else:
        return None,None

def check_order():
    """
    检查订货是否有异常的地方
    :return:
    """
    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d %H:%M:%S')
    week_ago = (now - datetime.timedelta(days=28)).strftime('%Y-%m-%d %H:%M:%S')
    sql = "select sum(p.amount),g.upc,g.corp_classify_code,g.neighbor_goods_id,g.price,p.name from dmstore.payment_detail as p left join dmstore.goods as g on p.goods_id=g.id where p.create_time > '{}' and p.create_time < '{}' and p.shop_id={} and g.upc='{}';"
    sql_02 = "select name from dmstore.goods where upc='{}';"
    sql_03 = "select delivery_type,storage_day from uc_merchant_goods where upc='{}';"


    # conn = pymysql.connect('123.103.16.19', 'readonly', password='fxiSHEhui2018@)@)', database='dmstore',charset="utf8", port=3300, use_unicode=True)
    conn = connections['dmstore']
    cursor = conn.cursor()
    conn_ucenter = connections['ucenter']
    cursor_ucenter = conn_ucenter.cursor()


    order_list = [{"max_disnums":3,"mch_goods_code":"2043054","min_disnums":1,"order_sale":2,"shelf_order_info":[{"face_num":2,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6940453400146"},{"max_disnums":6,"mch_goods_code":"2044177","min_disnums":4,"order_sale":24,"shelf_order_info":[{"face_num":2,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":5.0,"supply_stock":2.0,"upc":"6954767417684"},{"max_disnums":4,"mch_goods_code":"2042491","min_disnums":3,"order_sale":3,"shelf_order_info":[{"face_num":1,"shelf_id":1102,"shelf_order":0,"tz_id":1175}],"shop_stock":2.0,"supply_stock":0.0,"upc":"6923450664889"},{"max_disnums":5,"mch_goods_code":"2043552","min_disnums":1,"order_sale":2,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6907992102764"},{"max_disnums":17,"mch_goods_code":"2022117","min_disnums":1,"order_sale":5,"shelf_order_info":[{"face_num":2,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6902890234487"},{"max_disnums":5,"mch_goods_code":"2043546","min_disnums":1,"order_sale":1,"shelf_order_info":[{"face_num":2,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6944697601048"},{"max_disnums":11,"mch_goods_code":"2028823","min_disnums":1,"order_sale":2,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6957978700019"},{"max_disnums":11,"mch_goods_code":"2029926","min_disnums":1,"order_sale":2,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6957978700187"},{"max_disnums":3,"mch_goods_code":"2044981","min_disnums":1,"order_sale":1,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"20449810"},{"max_disnums":3,"mch_goods_code":"2045322","min_disnums":1,"order_sale":3,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6970182591884"},{"max_disnums":3,"mch_goods_code":"2043917","min_disnums":1,"order_sale":3,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6944697601161"},{"max_disnums":3,"mch_goods_code":"2045323","min_disnums":1,"order_sale":2,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"20453237"},{"max_disnums":3,"mch_goods_code":"2036958","min_disnums":1,"order_sale":4,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6943290507283"},{"max_disnums":3,"mch_goods_code":"2037707","min_disnums":1,"order_sale":1,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6943290507542"},{"max_disnums":11,"mch_goods_code":"2043895","min_disnums":1,"order_sale":1,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6970182590603"},{"max_disnums":11,"mch_goods_code":"2043893","min_disnums":1,"order_sale":3,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6970182590122"},{"max_disnums":11,"mch_goods_code":"2044730","min_disnums":1,"order_sale":1,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6970182591679"},{"max_disnums":11,"mch_goods_code":"2043892","min_disnums":1,"order_sale":2,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6970182590344"},{"max_disnums":5,"mch_goods_code":"2044985","min_disnums":1,"order_sale":1,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6932005206696"},{"max_disnums":8,"mch_goods_code":"2044563","min_disnums":1,"order_sale":1,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6932005206559"},{"max_disnums":4,"mch_goods_code":"2040128","min_disnums":3,"order_sale":3,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6922330913062"},{"max_disnums":6,"mch_goods_code":"2033796","min_disnums":1,"order_sale":1,"shelf_order_info":[{"face_num":1,"shelf_id":1096,"shelf_order":0,"tz_id":1169}],"shop_stock":0.0,"supply_stock":0.0,"upc":"6943290500949"}]


    merchant_dict = {1:'日配',2:'非日配',None:None}

    for d in order_list:
        print(d)
        # cursor.execute(sql.format(week_ago, now_date, 1284, d['upc']))
        # result = cursor.fetchone()
        # print(result)
        cursor.execute(sql_02.format(d['upc']))
        result_01 = cursor.fetchone()

        cursor_ucenter.execute(sql_03.format(d['upc']))
        result_02 = cursor_ucenter.fetchone()
        print('商品:{}'.format(result_01[0]),', 配送类型:{}'.format(merchant_dict[result_02[0]]),', 保质期（天）:{}'.format(result_02[1]))
        print()
        print()

if __name__ == '__main__':
    # calculate_goods_up_datetime(806)

    # calculate_goods_up_datetime_first(806)

    # print(select_psd_data('6921581540102',1284,28))

    check_order()