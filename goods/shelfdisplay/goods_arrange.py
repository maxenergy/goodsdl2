"""
输入：货架三级分类排列候选，货架内选品列表，三级分类的面积比例
输出：货架陈列
目标：总体得分最高

每层货架高度 = 当层商品最大高度+buff+层板高（可默认20mm）
商品扩面数 = n*psd/最大成列量（初始n默认为3）
spu：四级分类、品牌、规格（包装）、尺寸（只选宽和高）四个特征均相同，一个spu一起加入排序
强制条件：同品或同spu不拆分
根据算法4.1选品和算法4.2商品排列计算所有候选解。
根据算法4.3打分规则在给每个解打分后，获得最优解。
"""

from goods.shelfdisplay import single_algorithm
from goods.shelfdisplay import display_data

def goods_arrange(shelf, candidate_categoryid_list, goods_data_list, category_area_ratio, goods_arrange_weight):
    """

    :param shelf:货架
    :param candidate_categoryid_list: 货架三级分类排列候选
    :param goods_data_list: 候选商品
    :param category_area_ratio: 面积比例
    :param goods_arrange_weight: 商品排列权重
    :return:
    """

    # 一、准备工作
    # 1、计算扩面
    _solve_goods_face(shelf.depth, goods_data_list)
    # 2、计算spu
    # 3、每一个三级分类获得排序商品
    categoryid_to_sorted_goods_list = {}
    _caculate_shelf_category_area_ratio(shelf, candidate_categoryid_list[0], category_area_ratio)
    for categoryid in candidate_categoryid_list[0]:
        sorted_goods_list = single_algorithm.choose_goods_for_category3(categoryid, category_area_ratio, goods_data_list, shelf, extra_add=1)
        categoryid_to_sorted_goods_list[categoryid] = sorted_goods_list

    # 生成所有的候选解
    candidate_result_shelf_list = []
    for categoryid_list in candidate_categoryid_list:
        candidate_result_shelf_list.extend(
            _display_shelf(categoryid_list,categoryid_to_sorted_goods_list, shelf, goods_arrange_weight)
        )

    # 计算候选解的badcase得分
    best_shelf = single_algorithm.goods_badcase_score(candidate_result_shelf_list)

    shelf.assign(best_shelf)

    return True

def _display_shelf(categoryid_list, categoryid_to_sorted_goods_list, template_shelf, goods_arrange_weight):
    """
    主体陈列算法
    :param categoryid_list:
    :param categoryid_to_sorted_goods_list:
    :param template_shelf:
    :param goods_arrange_weight:
    :return:
    """
    candidate_result_shelf_list = []

    shelf = template_shelf.copy()
    for categoryid in categoryid_list:
        arrange_goods_list = single_algorithm.goods_arrange(categoryid_to_sorted_goods_list[categoryid][:-1], goods_arrange_weight)

        level = None
        for goods in arrange_goods_list:
            # 创建层
            level = _level_add_goods(shelf, level, goods)
            # TODO 什么情况以及如何才能再创建一个副本货架陈列

    return candidate_result_shelf_list

def _level_add_goods(shelf,cur_level,goods):
    """
    处理层添加和层的width和height变化
    :param shelf:
    :param levelid:
    :param goods:
    :return: 商品添加的层
    """

    ret_level = cur_level
    if cur_level == None:
        ret_level = display_data.Level()
        display_goods = display_data.DisplayGoods()
        ret_level.goods_list.append(display_goods)
        # TODO

    return ret_level

def _solve_goods_face(shelf_depth, goods_data_list):
    """
    扩面处理
    :param shelf_depth:
    :param goods_data_list:
    :return:
    """
    # TODO
    # TODO 层板深度问题处理怎么解决？
    pass

def _caculate_shelf_category_area_ratio(shelf, categoryid_list, category_area_ratio):
    """
    计算出本货架的比例
    :param shelf:
    :param categoryid_list:
    :param category_area_ratio:
    :return: 修正的category_area_ratio
    """

    shelf_category_area_ratio = {}
    # TODO
    return shelf_category_area_ratio
