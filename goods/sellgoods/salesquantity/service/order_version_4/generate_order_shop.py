"""
门店向二批补货  （1284 --> 1284）
"""
from set_config import config
import traceback
from goods.sellgoods.salesquantity.local_util import erp_interface
from goods.sellgoods.salesquantity.proxy import order_rule
from goods.sellgoods.salesquantity.service.order_version_5.data_util import cacul_util
shop_type = config.shellgoods_params['shop_types'][0]  # 门店
yinliao_cat_ids = config.shellgoods_params['yinliao_cat_ids'] # 饮料台账分类
def generate(shop_id = None):
    sales_order_inss = []
    try:
        print ("门店向二批补货,shop_id"+str(shop_id))
        if shop_id == None:
            return None
        result = cacul_util.data_process(shop_id,shop_type)
        print ("规则0 商品数："+str(len(result.keys())))
        for mch_code  in result:
            drg_ins = result[mch_code]
            # print ("规则1： 补货触发条件 商品的库存 < 最大陈列量   （饮料 ） ，  其他的<=最小陈列量")
            if (drg_ins.stock < drg_ins.max_disnums and drg_ins.category_id in yinliao_cat_ids)  or (drg_ins.stock <= drg_ins.min_disnums and drg_ins.category_id not in yinliao_cat_ids):
                order_sale = min(drg_ins.max_disnums-drg_ins.stock,drg_ins.supply_stock)
                if order_sale <= 0:
                    continue
                sales_order_ins = cacul_util.get_saleorder_ins(drg_ins, shop_id,shop_type)
                sales_order_ins.order_sale = order_sale
                sales_order_inss.append(sales_order_ins)
        sales_order_inss = order_rule.rule_filter_order_sale(sales_order_inss)
        print("规则三：商品数：" + str(len(sales_order_inss)))
        print("订货量,商品upc,商品名,最大陈列数,最小陈列数,门店库存,小仓库库存,保质期,配送类型,商品编码")
        for sales_order_ins in sales_order_inss:
            print("%s , %s, %s, %s, %s, %s, %s,%s,%s,%s" % (
                str(sales_order_ins.order_sale), str(sales_order_ins.upc), str(sales_order_ins.goods_name),
                str(sales_order_ins.max_stock), str(sales_order_ins.min_stock), str(sales_order_ins.stock),
                str(sales_order_ins.supply_stock),str(sales_order_ins.storage_day),str(sales_order_ins.delivery_type),str(sales_order_ins.mch_goods_code)))
    except Exception as e:
        print("add order failed  e = {}".format(e))
        traceback.print_exc()

        return None
    return sales_order_inss
if __name__=='__main__':
    generate(1284)