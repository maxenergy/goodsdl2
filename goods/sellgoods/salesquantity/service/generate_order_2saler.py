"""
二批向供货商订货  （1284 --> 好邻居）
"""
from set_config import config
from goods.sellgoods.salesquantity.local_util import erp_interface
from goods.sellgoods.salesquantity.proxy import order_rule
from goods.sellgoods.salesquantity.local_util import combean_to_mybean
from goods.goodsdata import get_shop_order_goods
order_shop_ids = config.shellgoods_params['order_shop_ids']
shop_type = config.shellgoods_params['shop_types'][1]  # 二批
def generate():
    for shop_id in order_shop_ids:
        result = get_shop_order_goods(shop_id,shop_type)
        sales_order_inss = []
        if result == None or len(result.keys()) < 1:
            print("shop_id day generate order failed ,get_data error   " + str(shop_id))
            return
        print ("规则0 商品数："+str(len(result.keys())))
        for mch_code  in result:
            drg_ins = result[mch_code]
            sales_order_ins = combean_to_mybean.get_saleorder_ins(drg_ins,shop_id,shop_type)
            sales_order_ins = order_rule.rule_isAndNotFir(sales_order_ins)
            if sales_order_ins != None:
                sales_order_inss.append(sales_order_ins)
        print("规则一：商品数：" + str(len(sales_order_inss)))
        sales_order_inss = order_rule.rule_start_sum(sales_order_inss)
        print("规则二：商品数：" + str(len(sales_order_inss)))
        sales_order_inss = order_rule.rule_filter_order_sale(sales_order_inss)
        print("规则三：商品数：" + str(len(sales_order_inss)))
        if len(sales_order_inss) > 0:
            erp_interface.order_commit(shop_id,shop_type,sales_order_inss)
            print("erp_interface.order_commit success!")

if __name__=='__main__':
    generate()