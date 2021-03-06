"""
初始化选品数据、分类比例、亲密度、上下层关系
初始化陈列相关的台账、货架、指定分类数据，最终生成初始化好的taizhang_display对象
"""

from django.db import connections


def init_base_data(uc_shopid, batch_id):
    """
    初始化基础数据：选品数据、分类比例、亲密度、上下层关系
    :param uc_shopid:
    :param batch_id:
    :return: BaseData
    """
    base_data = BaseData()
    # 获取数据
    cursor = connections['ucenter'].cursor()
    cursor_default = connections['default'].cursor()

    # 获取fx系统的shopid,台账系统的商家mch_id
    cursor.execute("select mch_shop_code,mch_id from uc_shop where id = {}".format(uc_shopid))
    (shopid, mch_id) = cursor.fetchone()

    # category_area_ratio: 分类陈列面积比例表
    base_data.category_area_ratio = {}
    cursor.execute(
        "select a.cat_id,a.ratio from sf_goods_categoryarearatio as a, sf_goods_shoptoshoptype as b where a.mch_id=b.mch_id and a.shop_type=b.shop_type and b.shop_id={}".format(
            uc_shopid))
    all_category_area_ratio = cursor.fetchall()
    for one in all_category_area_ratio:
        base_data.category_area_ratio[one[0]] = one[1]

    # category3_intimate_weight: 三级分类亲密度
    base_data.category3_intimate_weight = {}
    cursor.execute("select cat_ids, score from sf_goods_categoryintimacy where mch_id={}".format(mch_id))
    all_categoryintimacy = cursor.fetchall()
    for one in all_categoryintimacy:
        base_data.category3_intimate_weight[one[0]] = one[1]

    # category3_level_value: 三级分类层数分值
    base_data.category3_level_value = {}
    cursor.execute("select cat_id, score from sf_goods_categorylevelrelation where mch_id={}".format(mch_id))
    all_categorylevelrelation = cursor.fetchall()
    for one in all_categorylevelrelation:
        base_data.category3_level_value[one[0]] = one[1]

    # 获取选品数据（去除选品删除数据）
    cursor_default.execute(
        "select mch_goods_code, predict_sales_num, predict_sales_amount, goods_role, ranking, handle_goods_role from goods_goodsselectionhistory where shopid={} and batch_id='{}'".format(
            shopid, batch_id))
    all_selection_goods = cursor_default.fetchall()

    # 获取选品详细信息
    not_found_goods = 0
    mch_goods_code_list = []
    for selection_goods in all_selection_goods:
        # 获取商品属性
        mch_goods_code = selection_goods[0]
        goods_role = selection_goods[3]
        if goods_role == 5 or selection_goods[5] == 5: # handle_goods_role是人工操作的结果
            goods_role = 2
        # 做商品去重
        if mch_goods_code in mch_goods_code_list:
            continue
        mch_goods_code_list.append(mch_goods_code)
        try:
            cursor.execute(
                "select id, goods_name,upc, tz_display_img, display_first_cat_id, display_second_cat_id, display_third_cat_id, display_fourth_cat_id, package_type, brand, width,height,depth,is_superimpose,is_suspension from uc_merchant_goods where mch_id = {} and mch_goods_code = {}".format(
                    mch_id, mch_goods_code))
            (goods_id, goods_name, upc, tz_display_img, category1_id, category2_id, category3_id, category4_id, package_type, brand,
             width, height, depth, is_superimpose, is_suspension) = cursor.fetchone()

            # TODO 这里要做商品报警
            if category3_id is None:
                category3_id = ''
                print("商品{}({})没有设定三级分类".format(goods_name,mch_goods_code))
        except:
            not_found_goods += 1
            continue

        base_data.goods_data_list.append(GoodsData(mch_goods_code,
                                                   goods_name,
                                                   upc,
                                                   tz_display_img,
                                                   category1_id,
                                                   category2_id,
                                                   category3_id,
                                                   category4_id,
                                                   package_type,
                                                   brand,
                                                   width,
                                                   height,
                                                   depth,
                                                   is_superimpose,
                                                   is_suspension,
                                                   selection_goods[1],
                                                   selection_goods[2],
                                                   goods_role,
                                                   selection_goods[4]
                                                   ))

    print('找不到选品表的商品共有:{}个！'.format(not_found_goods))
    print('找到选品表的商品共有:{}个！'.format(len(base_data.goods_data_list)))
    cursor.close()
    cursor_default.close()

    return base_data


class BaseData:
    """
    category_area_ratio: 分类陈列面积比例表
    category3_intimate_weight: 三级分类亲密度
    category3_level_value: 三级分类层数分值
    goods_data_list: GoodsData列表
    """

    def __init__(self):
        self.category_area_ratio = None
        self.category3_intimate_weight = None
        self.category3_level_value = None
        self.goods_data_list = []

class NullGoodsData:
    def __init__(self, width):
        self.mch_code = ''
        self.goods_name = 'null'
        self.upc = ''
        self.tz_display_img = ''
        self.category1 = ''
        self.category2 = ''
        self.category3 = ''
        self.category4 = ''
        self.package_type = 0
        self.brand = ''
        self.layout = 1
        self.width = width
        self.height = 0
        self.depth = 0
        self.is_superimpose = 2  # 1可叠放，2不可叠放
        self.is_suspension = 2  # 1可挂放，2不可挂放
        self.psd = 0  # 预测销量
        self.psd_amount = 0 # 预测销售额
        self.face_num = 1  # 在某层陈列时填入
        self.add_face_num = 0  # 商品不足做扩面处理
        self.superimpose_num = 1  # 在商品初始化时填入
        self.goods_role = 3 # 商品的角色类型，0保护品，1上架，2下架，3可选上架，4可选下架'
        self.ranking = 0 # 该品为可选上下品时的优先级，越大越优先，可重复

    def equal(self, another_goods):
        return False

    def is_spu(self, another_goods):
        return False

    def height_diff(self, another_goods):
        if another_goods is not None:
            return (self.height * self.superimpose_num) - (another_goods.height - another_goods.superimpose_num)
        return 0

    def __str__(self):
        ret = '(null'
        ret += ','
        ret += str(self.width)
        ret += ')'
        return ret


class GoodsData:
    def __init__(self, mch_code, goods_name, upc, tz_display_img, category1, category2, category3, category4,
                 package_type, brand, width, height, depth, is_superimpose, is_suspension, psd, psd_amount, goods_role, ranking):
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
        self.layout = 1
        self.width = width
        self.height = height
        self.depth = depth
        if self.depth is None or self.depth == 0:
            self.depth = self.width
        self.is_superimpose = is_superimpose  # 1可叠放，2不可叠放
        self.is_suspension = is_suspension  # 1可挂放，2不可挂放
        if psd is None:
            psd = 0
        self.psd = psd  # 预测销量
        if psd_amount is None:
            psd_amount = 0
        self.psd_amount = psd_amount # 预测销售额
        self.face_num = 1  # 在某层陈列时填入
        self.add_face_num = 0  # 商品不足做扩面处理
        self.superimpose_num = 1  # 在商品初始化时填入
        self.goods_role = goods_role # 商品的角色类型，0保护品，1上架，2下架，3可选上架，4可选下架'
        self.ranking = ranking # 该品为可选上下品时的优先级，越大越优先，可重复

    def equal(self, another_goods):
        if another_goods is not None:
            return self.mch_code == another_goods.mch_code
        return False

    def is_spu(self, another_goods):
        if another_goods is not None:
            return self.category4 == another_goods.category4 and self.package_type == another_goods.package_type and self.brand == another_goods.brand \
                   and abs(self.height - another_goods.height) < 5 and abs(self.width - another_goods.width) < 5
        return False

    def height_diff(self, another_goods):
        if another_goods is not None:
            return (self.height * self.superimpose_num) - (another_goods.height - another_goods.superimpose_num)
        return 0

    def __str__(self):
        ret = '('
        ret += str(self.mch_code)
        ret += ','
        ret += str(self.goods_name)
        ret += ','
        # ret += str(self.upc)
        # ret += ','
        # ret += str(self.tz_display_img)
        # ret += ','
        # ret += str(self.category1)
        # ret += ','
        # ret += str(self.category2)
        # ret += ','
        ret += str(self.category3)
        ret += ','
        # ret += str(self.category4)
        # ret += ','
        ret += str(self.package_type)
        ret += ','
        ret += str(self.brand)
        ret += ','
        ret += str(self.height)
        ret += ','
        ret += str(self.width)
        ret += ','
        ret += str(self.depth)
        ret += ','
        ret += '%.2f' % (self.psd)
        ret += ')'
        return ret


class Category3:
    def __init__(self, category3, name, pid, average_height):
        self.category3 = category3
        self.name = name
        self.pid = pid
        self.average_height = average_height
