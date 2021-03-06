
import math
import collections
import copy,time
# from goods.goodsdata import *
# from goods.sellgoods.auto_display.drink_display import upc_statistics

def calculate_goods(taizhang):

    twidth_to_goods = collections.OrderedDict()
    mark = 0
    shelf_depth = taizhang.shelfs[0].depth
    for good in taizhang.calculate_goods_array:
        print("width,height,depth:",good.width,good.height,good.depth)
        # good.display_num = max(good.sale_num*2,good.start_num)
        good.one_face_most_goods_num = int(shelf_depth/good.depth)
        if good.is_superimpose:   # 可叠放
            good.one_face_most_goods_num = good.one_face_most_goods_num*good.superimpose_rows

        t = math.ceil(good.start_num/good.one_face_most_goods_num)

        good.faces_num = max(math.ceil(t),1)       # math.ceil()进一法
        good.display_num = good.faces_num * good.one_face_most_goods_num
        good.good_scale = good.faces_num*good.width

        mark += good.good_scale
        twidth_to_goods[mark] = (good,0)     # 第二个代表该品在货架上已经摆过的face数
        # twidth_to_goods[good.mch_good_code] = mark

    taizhang.twidth_to_goods = twidth_to_goods
    taizhang.last_twidth = mark

def update_mark_goods_array_origin(taizhang,change_total_width):
    """
    更新货架所需的商品的刻度
    :param taizhang:
    :param change_total_width: 改变的宽度
    :return:
    """

    # if change_total_width < 0:
    #     sum = 0
    #     reversed_calculate_goods_array = list(reversed(taizhang.calculate_goods_array))
    #     for good in reversed_calculate_goods_array:
    #         a = math.fabs(change_total_width) - sum
    #         sum += good.good_scale
    #         b = sum - math.fabs(change_total_width)
    #         if a > 0 and b > 0:
    #             good_index = taizhang.calculate_goods_array.index(good)
    #             if a > b:
    #                 taizhang.last_twidth = taizhang.twidth_to_goods(taizhang.calculate_goods_array[good_index-1].mch_good_code)
    #             else:
    #                 taizhang.last_twidth = taizhang.twidth_to_goods(taizhang.calculate_goods_array[good_index].mch_good_code)
    #
    # if change_total_width > 0:
    #     pass
    old_mark = taizhang.last_twidth
    new_mark = None
    tem = []
    for mark,good in taizhang.twidth_to_goods.items():
        if mark < taizhang.last_twidth + change_total_width:
            tem.append(good[0])
            new_mark = mark

    taizhang.calculate_goods_array = tem
    if old_mark == new_mark:
        return False
    else:
        taizhang.last_twidth = new_mark
        return True

def shelf_gap_expand_gooods_origin(taizhang):
    """
    对于每层的空隙，进行周边商品增加face来填充
    :param taizhang:
    :return:
    """
    result_list = []
    for shelf in taizhang.shelfs:
        for level in shelf.levels:
            if level.level_none_good_width > level.goods[-1].width:
                add_face_num = 1     # 增加的face数
                while level.level_none_good_width > add_face_num * level.goods[-1].width:
                    add_face_num += 1
                add_face_num -= 1
                gap_good = copy.deepcopy(level.goods[-1])
                gap_good.faces_num = add_face_num
                gap_good.display_num = gap_good.faces_num * gap_good.one_face_most_goods_num
                gap_good.good_scale = gap_good.faces_num * gap_good.width
                result_list.append((shelf.shelf_id, level.level_id, [gap_good]))
    return result_list

def shelf_gap_choose_goods_origin(taizhang):
    """
    空隙补品
    :param taizhang:
    :param neighbour_good:  最近的商品的三级类
    :param level_goods:  这一层的商品的三级类
    :param level_diff_width:  空隙的宽度
    :return:
    """

    result_list = []
    goods_list = []
    for shelf in taizhang.shelfs:
        for level in shelf.levels:
            level.temp_gap = level.level_none_good_width


    # 不拆的情况下，最近邻商品同小类
    for k,v in taizhang.twidth_to_goods.items():
        if k > taizhang.last_twidth:          # 在已选择商品的刻度之后
            for shelf in taizhang.shelfs:
                for level in shelf.levels:
                    # print('first')
                    if level.goods[-1].third_cls_code == v[0].third_cls_code:   # 和旁边最近的同属一个小类
                        if level.temp_gap > v[0].good_scale:  # 缝隙比商品不拆分的情况下的宽要宽
                            if v[0].height <= level.level_height:
                                result_list.append((shelf.shelf_id,level.level_id,[v[0]]))
                                level.temp_gap = level.temp_gap - v[0].good_scale
                                goods_list.append(v[0])
                                break
                break

    # 不拆的情况下，同层商品同小类
    for k, v in taizhang.twidth_to_goods.items():
        if k > taizhang.last_twidth:  # 在已选择商品的刻度之后
            for shelf in taizhang.shelfs:
                for level in shelf.levels:
                    for good in level.goods:
                        # print("second")
                        if good.third_cls_code == v[0].third_cls_code:   # 和这层任一商品同属一个小类
                            if level.temp_gap > v[0].good_scale:  # 剩下的缝隙比商品不拆分的情况下的宽要宽
                                if not v[0] in goods_list:
                                    if v[0].height <= level.level_height:
                                        result_list.append((shelf.shelf_id,level.level_id,[v[0]]))
                                        level.temp_gap = level.temp_gap - v[0].good_scale
                                        goods_list.append(v[0])
                                        break
                    break
                break


    # # 拆的情况下
    # for shelf in taizhang.shelfs:
    #     goods_list_02 = []
    #     for level in shelf.levels:
    #         # 拆的情况下，最近邻商品同小类
    #         for k, v in taizhang.twidth_to_goods.items():
    #             # print('third')
    #             if k > taizhang.last_twidth:  # 在已选择商品的刻度之后
    #                 if level.goods[-1].third_cls_code == v[0].third_cls_code:  # 和旁边最近的同属一个小类
    #                     if v[1] > 0:   # 该商品被陈列过
    #                         if v[0].mch_good_code in goods_list_02:   #该商品之前是在本货架陈列过
    #                             t = 1
    #                             # while level.temp_gap > v[0].width * t:
    #                             #     t += 1
    #                             # t -= 1
    #                             # if level.temp_gap > v[0].good_scale - v[1] * (v[0].width):  # 缝隙比商品可陈列的宽要宽
    #                             #     new_good = copy.deepcopy(v[0])
    #                             #     new_good.faces_num = v[0].faces_num - v[1]
    #                             #     new_good.good_scale = new_good.good_scale * (new_good.faces_num/v[0].faces_num)
    #                             #     new_good.display_num = v[0].display_num - new_good.faces_num * v[0].one_face_most_goods_num
    #                             #     result_list.append((shelf.shelf_id, level.level_id, new_good))
    #                             #     level.temp_gap = level.temp_gap - new_good.good_scale
    #                             # else:
    #                             #     pass
    #
    #                     else:   # 该商品没被陈列过
    #                         if not v[0] in goods_list:   # 该商品之前也没被陈列过
    #                             if level.temp_gap > v[0].width:  # 缝隙比商品的宽要宽
    #                                 t =1
    #                                 while level.temp_gap > v[0].width * t:
    #                                     t += 1
    #                                 t -= 1
    #                                 new_good = copy.deepcopy(v[0])
    #                                 new_good.faces_num = t
    #                                 new_good.good_scale = new_good.width * t
    #                                 new_good.display_num = t * new_good.one_face_most_goods_num
    #                                 result_list.append((shelf.shelf_id, level.level_id, new_good))
    #                                 level.temp_gap = level.temp_gap - new_good.good_scale
    #                                 v[1] = t
    #                                 goods_list_02.append(v[0].mch_good_code)
    #         # 拆的情况下，同层商品同小类
    #         for k, v in taizhang.twidth_to_goods.items():
    #             if k > taizhang.last_twidth:  # 在已选择商品的刻度之后
    #                 for good in level.goods:
    #                     print("third_02")
    #                     if good.third_cls_code == v[0].third_cls_code:   # 和这层任一商品同属一个小类
    #
    #                         if v[1] > 0:   # 该商品被陈列过
    #                             if v[0].mch_good_code in goods_list_02:   #该商品之前是在本货架陈列过
    #                                 if level.temp_gap > v[0].good_scale-v[1]*(v[0].good_scale/v[0].faces_num):  # 缝隙比商品可陈列的宽要宽
    #                                     new_good = copy.deepcopy(v[0])
    #                                     new_good.faces_num = v[0].faces_num - v[1]
    #                                     new_good.good_scale = new_good.good_scale * (new_good.faces_num/v[0].faces_num)
    #                                     new_good.display_num = v[0].display_num - new_good.faces_num * v[0].one_face_most_goods_num
    #                                     result_list.append((shelf.shelf_id, level.level_id, new_good))
    #                                     level.temp_gap = level.temp_gap - new_good.good_scale
    #                         else:   # 该商品没被陈列过
    #                             if not v[0] in goods_list:   # 该商品之前也没被陈列过
    #                                 if level.temp_gap > v[0].width:  # 缝隙比商品可陈列的宽要宽
    #                                     t =1
    #                                     while level.temp_gap > v[0].width * t:
    #                                         t += 1
    #                                     t -= 1
    #                                     new_good = copy.deepcopy(v[0])
    #                                     new_good.faces_num = t
    #                                     new_good.good_scale = new_good.width * t
    #                                     new_good.display_num = t * new_good.one_face_most_goods_num
    #                                     result_list.append((shelf.shelf_id, level.level_id, new_good))
    #                                     level.temp_gap = level.temp_gap - new_good.good_scale
    #                                     v[1] = t
    #                                     goods_list_02.append(v[0].mch_good_code)

    return result_list


