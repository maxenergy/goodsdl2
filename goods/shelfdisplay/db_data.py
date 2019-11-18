from django.db import connections
from goods.models import FirstGoodsSelection

"""
ShareData
GoodsData
"""


def init_data(uc_shopid):
    base_data = BaseData()
    # 获取数据
    cursor = connections['ucenter'].cursor()

    # 获取fx系统的shopid,台账系统的商家mch_id
    cursor.execute("select mch_shop_code,mch_id from uc_shop where id = {}".format(uc_shopid))
    (shopid, mch_id) = cursor.fetchone()

    # category_area_ratio: 分类陈列面积比例表
    cursor.execute("select a.cat_id,a.ratio from sf_goods_categoryarearatio as a, sf_goods_shoptoshoptype as b where a.mch_id=b.mch_id and a.shop_type=b.shop_type and b.shop_id={}".format(uc_shopid))
    all_category_area_ratio = cursor.fetchall()
    for one in all_category_area_ratio:
        base_data.category_area_ratio[one[0]] = one[1]

    # category3_intimate_weight: 三级分类亲密度
    cursor.execute("select cat_ids, score from sf_goods_categoryintimacy where mch_id={}".format(mch_id))
    all_categoryintimacy = cursor.fetchall()
    for one in all_categoryintimacy:
        base_data.category3_intimate_weight[one[0]] = one[1]

    # category3_level_value: 三级分类层数分值
    cursor.execute("select cat_id, score from sf_goods_categorylevelrelation where mch_id={}".format(mch_id))
    all_categorylevelrelation = cursor.fetchall()
    for one in all_categorylevelrelation:
        base_data.category3_level_value[one[0]] = one[1]

    # 获取选品数据
    all_selection_goods = FirstGoodsSelection.objects.filter(shopid=shopid)

    # 获取选品详细信息
    for selection_goods in all_selection_goods:
        # 获取商品属性
        mch_goods_code = selection_goods.mch_goods_code
        try:
            cursor.execute("select id, goods_name,upc, tz_display_img, category1_id, category2_id, category_id, package_type, brand, width,height,depth,is_superimpose,is_suspension from uc_merchant_goods where mch_id = {} and mch_goods_code = {}".format(mch_id, mch_goods_code))
            (goods_id, goods_name, upc, tz_display_img, category1_id, category2_id, category3_id, package_type, brand, width, height, depth,is_superimpose,is_suspension) = cursor.fetchone()
            # FIXME width,height暂时翻转
            # (goods_id, goods_name, upc, tz_display_img, spec, volume, height, width, depth, is_superimpose, is_suspension) = cursor.fetchone()
        except:
            print('台账找不到商品，只能把这个删除剔除:{}！'.format(mch_goods_code))
            continue

        base_data.goods_data_list.append(GoodsData(mch_goods_code,
                             goods_name,
                             upc,
                             tz_display_img,
                             category1_id,
                             category2_id,
                             category3_id,
                             None,
                             package_type,
                             brand,
                             width,
                             height,
                             depth,
                             is_superimpose,
                             is_suspension,
                             selection_goods.predict_sales_num))

    cursor.close()

    return base_data

class BaseData:
    """
    category_area_ratio: 分类陈列面积比例表
    category3_intimate_weight: 三级分类亲密度
    category3_level_value: 三级分类层数分值
    goods_data_list: GoodsData列表
    """
    category_area_ratio = {'a': 0.1, 'b': 0.2, 'c': 0.3, 'd': 0.4, 'e': 0.5}
    category3_intimate_weight = {'a,b': 10, 'a,b,c': 5, 'd,e': 10, 'd,e,f': 5, 'd,e,f,g': 3}
    category3_level_value = {'b': 0, 'c': 10}
    goods_data_list = []

class GoodsData:
    """
    商品的纯信息数据
    """
    mch_code = None
    goods_name = None
    upc = None
    tz_display_img = None
    category1 = None
    category2 = None
    category3 = None
    category4 = None
    package_type = None # 包装方式
    brand = None # 品牌
    width = None
    height = None
    depth = None
    is_superimpose = None # 1可叠放，2不可叠放
    is_suspension = None # 1可挂放，2不可挂放
    psd = None # 预测销量

    face_num = 1 #在某个货架时填入 # FIXME 临时方案
    superimpose_num = 1 #在商品初始化时填入

    def __init__(self, mch_code, goods_name, upc, tz_display_img, category1, category2, category3, category4, package_type, brand, width, height, depth, is_superimpose, is_suspension, psd):
        self.mch_code = mch_code
        self.goods_name = goods_name
        self.upc = upc
        self.tz_display_img = tz_display_img
        self.category1 = category1
        self.category2 = category2
        self.category3 = category3
        self.category4 = category4
        self.package_type = package_type
        self.brand = brand
        self.width = width
        self.height = height
        self.depth = depth
        self.is_superimpose = is_superimpose
        self.is_suspension = is_suspension
        self.psd = psd

    def equal(self, another_goods):
        if another_goods is not None:
            return self.mch_code == another_goods.mch_code
        return False

    def is_spu(self, another_goods):
        if another_goods is not None:
            return self.category4 == another_goods.category4 and self.package_type == another_goods.package_type and self.brand == another_goods.brand \
                   and abs(self.height - another_goods.height) < 5 and abs(self.width - another_goods.width) < 5
        return False

    def height_diff(self,another_goods):
        if another_goods is not None:
            # FIXME 需考虑叠放
            return self.height - another_goods.height
        return 0



