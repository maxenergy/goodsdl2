"""
算法说明：
排序规则中，亲密度优先
根据得分排序组合，输出多个符合要求的排序组合
组合内的层数分值说明：假设组合（a，b，c）
a，b，c如分值都大于5，则以最大的计算
a，b，c如分值都小于5，则以最小的计算
a，b，c如分值既有大于5又有小于5，则为N（未定义）
"""
import itertools
import math
from functools import reduce

from goods.shelfdisplay.normal_algorithm import dict_arrange
from goods.third_tools import dingtalk


def shelf_arrange(shelf):
    """
    流程：
        先全部无约束的排序
        然后根据亲密度条件筛选
        然后根据上下关系筛选
    :param shelf: display_data中的shelf对象
    :return: 候选分类列表，例如[[a,b,c,d],[d,c,b,a]]
    """
    category3_to_category3_obj = shelf.shelf_category3_to_category3_obj
    category3_intimate_weight = shelf.shelf_category3_intimate_weight
    category3_level_value = shelf.shelf_category3_level_value

    return main_calculate(category3_to_category3_obj, category3_intimate_weight, category3_level_value)


def main_calculate(category3_to_category3_obj, category3_intimate_weight, category3_level_value):
    """
    根据亲密度，层数分计算
    :param category3_to_category3_obj: 三级分类详细信息
    :param category3_intimate_weight: 亲密度
    :param category3_level_value: 层数分
    :return: 总体后选列表
    """

    # FIXME 做CategoryTree.one_category_combination_threshhold的限制
    len_category3 = len(category3_to_category3_obj)
    if len_category3 > 10 and len_category3 <= 20:
        CategoryTree.one_category_combination_threshhold = 5
    elif len_category3 > 20:
        CategoryTree.one_category_combination_threshhold = 2

    # 1，初始化数据
    root_category_tree = init_category_tree(category3_to_category3_obj, category3_intimate_weight,
                                            category3_level_value)

    # print(root_category_tree)
    # 2，计算level_value
    root_category_tree.calculate_level_value()
    # print(root_category_tree)

    # 3, 输出组合
    root_category_tree.calculate_result()
    # print(root_category_tree)

    return root_category_tree.get_all_simple_result()


def init_category_tree(category3_to_category3_obj, category3_intimate_weight, category3_level_value):
    """

    :param category3_to_category3_obj:
    :param category3_intimate_weight:
    :param category3_level_value:
    :return:
    """
    # 获取所有2级分类的分组
    category2_to_category3_list = {}
    for category3 in category3_to_category3_obj.keys():
        category3_obj = category3_to_category3_obj[category3]
        if category3_obj.pid in category2_to_category3_list:
            category2_to_category3_list[category3_obj.pid].append(category3)
        else:
            category2_to_category3_list[category3_obj.pid] = [category3]

    tree_id = 1
    root_tree_list = []
    for category2 in category2_to_category3_list.keys():
        # 筛选三个参数
        one_category3_list = category2_to_category3_list[category2]
        one_category3_intimate_weight = {}
        one_category3_level_value = {}
        for category3 in one_category3_list:
            for category3_list_str in category3_intimate_weight.keys():
                # 做部分删减
                category3_list = category3_list_str.split(',')
                if category3 in category3_list:
                    one_category3_intimate_weight[category3_list_str] = category3_intimate_weight[
                        category3_list_str]
            if category3 in category3_level_value:
                one_category3_level_value[category3] = category3_level_value[category3]

        one_root_tree = init_one_category2_tree(category3_to_category3_obj, one_category3_intimate_weight, one_category3_level_value,
                                                one_category3_list, tree_id=tree_id)
        root_tree_list.append(one_root_tree)
        tree_id = one_root_tree.id + 1

    category2_tree_root = CategoryTree(tree_id, 0)
    category2_tree_root.init_parent(root_tree_list)
    print('init category2_tree_root finish')
    return category2_tree_root


def init_one_category2_tree(category3_to_category3_obj, category3_intimate_weight, category3_level_value,
                            category3_list, tree_id=1):
    """
    返回CategoryTree列表，初始类似的结构：（（a，b），c），（（d，e），f），g）
    a、b	=10
    a、b、c=5
    d、e	=10
    d、e、f=6
    d、e、f、g=5

    :param category3_to_category3_obj
    :param category3_intimate_weight:
    :param category3_level_value:
    :param category3_list:
    :return:
    """

    intimate_list = []  # 属于这个货架的亲密度的列表
    for group, value in category3_intimate_weight.items():  # 遍历每个亲密度
        belong_part_category3 = []  # 亲密度中属于这个货架的那几个三级分类
        for i in group.split(','):
            if i in category3_list:
                belong_part_category3.append(i)
        if len(belong_part_category3) > 1:  # 长度等于1或者0，亲密度就没意义了
            intimate_list.append([belong_part_category3, value])  # 列表套列表[[[a,b],10],[[d,e,f],5]]
    # 以下是去重
    intimate_list_temp_category = []
    intimate_list_temp = []
    for i in intimate_list:
        if not i[0] in intimate_list_temp_category:
            intimate_list_temp.append(i)
            intimate_list_temp_category.append(i[0])
        else:
            for t in intimate_list_temp:
                if t[0] == i[0]:  # 如果重复，要分值高得那个
                    if i[1] > t[1]:
                        t[1] = i[1]
    category3_intimate_weight = {}
    for i in intimate_list_temp:
        category3_intimate_weight[",".join(i[0])] = i[1]

    print('新的category3_intimate_weight', category3_intimate_weight)
    # TODO 处理掉category3_list没有，但category3_intimate_weight有的三级分类

    sorted_intimate_list = sorted(category3_intimate_weight.items(), key=lambda item: item[1], reverse=True)
    # print(sorted_intimate_list)

    all_category_tree_without_parent = []
    all_intimate_category_tree_only_parent = []

    for intimate in sorted_intimate_list:
        cat_ids = intimate[0]
        intimate_value = intimate[1]
        category_list = cat_ids.split(',')
        if len(category_list) <= 0:
            print('cat_ids is error:{}'.format(cat_ids))
            continue
        category_to_category_tree = {}
        is_found = False
        all_found = True
        for category3 in category_list:
            found_category = _find_category(category3, all_category_tree_without_parent)
            category_to_category_tree[category3] = found_category
            if found_category is not None:
                is_found = True
            if found_category is None:
                all_found = False

        if is_found:
            # 增量创建
            if all_found:
                # 1、parent和parent组合
                id_to_parent_tree = {}
                for category3 in category_to_category_tree.keys():
                    parent = category_to_category_tree[category3].parent
                    id_to_parent_tree[parent.id] = parent
                category_tree_parent = CategoryTree(tree_id, intimate_value)
                tree_id += 1
                category_tree_parent.init_parent(id_to_parent_tree.values())
                all_intimate_category_tree_only_parent.append(category_tree_parent)

            else:
                # 查找最小的亲密度值
                min_intimate_value = 1000
                min_intimate_parent_tree = None
                for category3 in category_to_category_tree.keys():
                    if category_to_category_tree[category3] is not None:
                        if category_to_category_tree[category3].intimate_value < min_intimate_value:
                            min_intimate_value = category_to_category_tree[category3].intimate_value
                            min_intimate_parent_tree = category_to_category_tree[category3].parent

                if min_intimate_value == intimate_value:
                    # 2、在一个存在的parent下面创建一个叶子
                    for category3 in category_to_category_tree.keys():
                        if category_to_category_tree[category3] is None:
                            category_tree = CategoryTree(tree_id, intimate_value)
                            tree_id += 1
                            category_tree.init_child_with_parent(category3, min_intimate_parent_tree)
                            all_category_tree_without_parent.append(category_tree)
                elif min_intimate_value > intimate_value:
                    # 3、扩层创建，和一个parent同层创建，并组合创建共同的parent
                    category_tree_leaf_list = []
                    category_tree_leaf_list.append(min_intimate_parent_tree)
                    for category3 in category_to_category_tree.keys():
                        if category_to_category_tree[category3] is None:
                            category_tree = CategoryTree(tree_id, intimate_value)
                            tree_id += 1
                            category_tree.init_only_child(category3)
                            category_tree_leaf_list.append(category_tree)
                            all_category_tree_without_parent.append(category_tree)
                    category_tree_parent = CategoryTree(tree_id, intimate_value)
                    tree_id += 1
                    category_tree_parent.init_parent(category_tree_leaf_list)
                    all_intimate_category_tree_only_parent.append(category_tree_parent)
        else:
            # 4、全新创建
            category_tree_leaf_list = []
            for category3 in category_list:
                category_tree = CategoryTree(tree_id, intimate_value)
                tree_id += 1
                category_tree.init_only_child(category3)
                category_tree_leaf_list.append(category_tree)
                all_category_tree_without_parent.append(category_tree)
            category_tree_parent = CategoryTree(tree_id, intimate_value)
            tree_id += 1
            category_tree_parent.init_parent(category_tree_leaf_list)
            all_intimate_category_tree_only_parent.append(category_tree_parent)

    id_to_intimate_root_parent_tree = {}
    for parent_tree in all_intimate_category_tree_only_parent:
        if parent_tree.parent == None:
            id_to_intimate_root_parent_tree[parent_tree.id] = parent_tree

    all_root_tree_children = []
    for id in id_to_intimate_root_parent_tree.keys():
        all_root_tree_children.append(id_to_intimate_root_parent_tree[id])

    # 创建不在亲密度里面的三级分类
    top_create_category3_list = []
    for category3 in category3_list:
        found_category = _find_category(category3, all_category_tree_without_parent)
        if not found_category:
            top_create_category3_list.append(category3)

    top_category3_create_num = len(top_create_category3_list)
    if top_category3_create_num > 4:
        # 根据高度做4，4分组
        category3_obj_list = []
        for category3 in top_create_category3_list:
            category3_obj_list.append(category3_to_category3_obj[category3])
        sorted_category3_obj_list = sorted(category3_obj_list, key=lambda item: item.average_height, reverse=True)
        need_create_category3_2dlist = []
        for i in range(math.ceil(top_category3_create_num/4)):
            one_list = []
            for j in range(4):
                if i*4+j >= top_category3_create_num:
                    break
                one_list.append(sorted_category3_obj_list[i*4+j].category3)
            if len(one_list) > 0:
                need_create_category3_2dlist.append(one_list)

        category_tree_parent_list = []
        for one_level in need_create_category3_2dlist:
            child_category_tree_list = []
            for category3 in one_level:
                category_tree = CategoryTree(tree_id, 0)
                tree_id += 1
                category_tree.init_only_child(category3)
                all_category_tree_without_parent.append(category_tree)
                child_category_tree_list.append(category_tree)
            category_tree_parent = CategoryTree(tree_id, 0)
            tree_id += 1
            category_tree_parent.init_parent(child_category_tree_list)
            category_tree_parent_list.append(category_tree_parent)
        another_category3_root_tree = CategoryTree(tree_id, 0)
        tree_id += 1
        another_category3_root_tree.init_parent(category_tree_parent_list)
        all_root_tree_children.append(another_category3_root_tree)
    elif top_category3_create_num >= 1:
        for category3 in top_create_category3_list:
            category_tree = CategoryTree(tree_id, 0)
            tree_id += 1
            category_tree.init_only_child(category3)
            all_category_tree_without_parent.append(category_tree)
            all_root_tree_children.append(category_tree)

    # 初始化非节点tree的level_value
    for child_tree in all_category_tree_without_parent:
        if child_tree.category in category3_level_value:
            child_tree.level_value = category3_level_value[child_tree.category]

    category_tree_root = CategoryTree(tree_id, 100)
    category_tree_root.init_parent(all_root_tree_children)
    return category_tree_root


def _find_category(category, category_tree_list):
    for category_tree in category_tree_list:
        ret = category_tree.find(category)
        if ret is not None:
            return ret

    return None


class CategoryTree:
    one_category_combination_threshhold = 10 # 一个分类组合阈值需要根据实际情况计算
    all_category_combination_threshhold = 100 # 所有分类组合的阈值

    def __init__(self, id, intimate_value):
        self.id = id
        self.intimate_value = intimate_value
        self.children = None
        self.parent = None
        self.level_value = None
        self.category = None
        self.result_list = None  # 这里面是对象解：[(Child1,Child2,Child3),(Child2,Child3,Child1)]

    def init_only_child(self, category):
        # 初始叶子对象
        self.category = category

    def init_child_with_parent(self, category, parent):
        # 后续叶子对象
        self.category = category
        self.parent = parent
        parent.children.append(self)

    def init_parent(self, category_tree_children):
        # 组合节点
        self.children = []
        for category_tree in category_tree_children:
            self.children.append(category_tree)
            category_tree.parent = self

    def find(self, category):
        if self.children is None:
            if self.category == category:
                return self
        else:
            for child in self.children:
                ret = child.find(category)
                if ret is not None:
                    return ret

        return None

    def calculate_level_value(self):
        min_level_value = 10
        max_level_value = 0
        if self.children is not None:
            for child in self.children:
                if child.children is not None:
                    child.calculate_level_value()
                if child.level_value is not None:
                    if child.level_value < min_level_value:
                        min_level_value = child.level_value
                    if child.level_value > max_level_value:
                        max_level_value = child.level_value
            if min_level_value <= max_level_value:
                # 出现有效值
                if min_level_value > 5:
                    self.level_value = max_level_value
                if max_level_value < 5:
                    self.level_value = min_level_value

    def calculate_result(self):
        """

        :param threshold: 最大排列数的阈值
        :return:
        """

        if self.children is not None:
            for child in self.children:
                if child.children is not None:
                    child.calculate_result()

            self.result_list = []
            # temp_result = arrange_all(self.children)

            iter = itertools.permutations(self.children, len(self.children))  # 所有排列的生成器
            list_len = len(self.children)

            if list_len > 8:
                msg = '候选解太多：{}'.format(str(self))
                dingtalk.send_message(msg, 2)
                raise ValueError(msg)
            max_length = reduce(lambda x, y: x * y, range(1, list_len + 1))  # 阶乘
            if max_length > self.one_category_combination_threshhold:  # 如果大于阈值，则根据步长设置进行下采样
                step_size = math.ceil(max_length / self.one_category_combination_threshhold)
            else:
                step_size = 1

            j = -1
            for i, one_result in enumerate(iter):
                # if random.random() > 1 // step_size:  # 进行下采样
                #     continue
                # else:

                last_category_tree = None
                is_valid = True
                for category_tree in one_result:
                    if last_category_tree is not None:
                        if last_category_tree.level_value is None and category_tree.level_value == 0:
                            is_valid = False
                            break
                        if category_tree.level_value is None and last_category_tree.level_value == 10:
                            is_valid = False
                            break
                        if last_category_tree.level_value is not None and category_tree.level_value is not None and last_category_tree.level_value > category_tree.level_value:
                            is_valid = False
                            break
                    last_category_tree = category_tree
                if is_valid:
                    j += 1
                    if j % step_size == 0:  # 进行下采样
                        self.result_list.append(one_result)
            if len(self.result_list) == 0:
                msg = '货架层级规则导致没有有效解: {}'.format(str(self))
                dingtalk.send_message(msg, 2)
                raise ValueError(msg)

    def get_all_simple_result(self):
        if self.children is not None:
            all_simple_result = []
            if self.parent is None:
                j = -1
            for result in self.result_list:
                index = 0
                index_to_simple_result_list = {}
                for one_tree in result:
                    if one_tree.children is not None:
                        child_all_simple_result = one_tree.get_all_simple_result()
                        index_to_simple_result_list[index] = child_all_simple_result
                        index += 1
                    else:
                        index_to_simple_result_list[index] = [one_tree.category]
                        index += 1
                # try:
                list_index_to_simple_result = dict_arrange(index_to_simple_result_list)
                # except:
                #     print(1)
                if self.parent is None:
                    max_length = len(list_index_to_simple_result)
                    if max_length > self.all_category_combination_threshhold:  # 如果大于阈值，则根据步长设置进行下采样
                        step_size = math.ceil(max_length / self.all_category_combination_threshhold)

                    else:
                        step_size = 1

                for index_to_simple_result in list_index_to_simple_result:
                    if self.parent is None:
                        j += 1
                    if self.parent is not None or j % step_size == 0:  # 进行下采样
                        simple_result_list = []
                        for i in range(index):
                            if type(index_to_simple_result[i]) is list:
                                for one_simple in index_to_simple_result[i]:
                                    simple_result_list.append(one_simple)
                            else:
                                simple_result_list.append(index_to_simple_result[i])
                        all_simple_result.append(simple_result_list)
            return all_simple_result

    def __str__(self):
        ret = ''
        if self.children is None:
            return str(self.level_value) + ':' + str(self.category) + ','
        else:
            if self.result_list is not None:
                ret += str(self.level_value)
                ret += '-'
                ret += str(len(self.result_list))
                ret += ':('
                for child in self.children:
                    ret += str(child)
                ret += '),'

                # if self.parent is None:
                #     ret += '\n'
                #     simple_results = self.get_all_simple_result()
                #     ret += str(len(simple_results))
                #     ret += '-'
                #     ret += str(simple_results)
            else:
                ret += str(self.level_value)
                ret += ':('
                for child in self.children:
                    ret += str(child)
                ret += '),'

        return ret


class Category3Demo:
    def __init__(self, category3, name, pid, average_height):
        self.category3 = category3
        self.name = name
        self.pid = pid
        self.average_height = average_height


if __name__ == '__main__':
    # TODO 李树
    category3_intimate_weight = [
        {'a,b': 10, 'a,b,c': 5, 'd,e': 10, 'd,e,f': 6, 'd,e,f,g': 5},
        {},
        {'a,b': 10, 'a,b,c': 5, 'd,a': 10, 'd,e,f': 6, 'd,e,f,g': 5},
        {'a,b': 10, 'a,b,c': 5, 'd,e': 10, 'd,e,f': 6, 'd,e,f,g': 5},
        {'a,b': 10, 'a,b,c': 5, 'd,e': 10, 'd,e,f': 6, 'd,e,f,g': 5},
        {'a,b': 10, 'a,b,c': 5, 'd,e': 10, 'd,e,m': 8, 'd,e,f,g,h,i,j,k,l,m': 5},
        {'a,b': 10, 'a,b,c': 5, 'd,e': 10, 'd,e,f': 6, 'd,e,f,g': 5},
    ]
    category3_level_value = [
        {'b': 8, 'c': 10, 'e': 0},
        {},
        {'b': 8, 'c': 10, 'e': 0},
        {'b': 8, 'c': 10, 'e': 0},
        {'b': 10, 'c': 0, 'e': 0, 'a': 0},
        {'b': 8, 'c': 10, 'e': 0},
        {'b': 8, 'c': 10, 'e': 0},
        {'b': 8, 'c': 10, 'e': 10},
    ]
    category3_to_category3_obj = [
        {'a': Category3Demo('a', 'a', 'A', 200),
         'b': Category3Demo('b', 'b', 'A', 200),
         'c': Category3Demo('c', 'c', 'A', 200),
         'd': Category3Demo('d', 'd', 'A', 200),
         'e': Category3Demo('e', 'e', 'A', 200),
         'f': Category3Demo('f', 'f', 'A', 200),
         'g': Category3Demo('g', 'g', 'A', 200)
         },
        {'a': Category3Demo('a', 'a', 'A', 200),
         'b': Category3Demo('b', 'b', 'A', 200),
         'c': Category3Demo('c', 'c', 'A', 200),
         'd': Category3Demo('d', 'd', 'A', 200),
         'e': Category3Demo('e', 'e', 'A', 200),
         'f': Category3Demo('f', 'f', 'A', 200),
         'g': Category3Demo('g', 'g', 'A', 200)
         },
        {'a': Category3Demo('a', 'a', 'A', 200),
         'b': Category3Demo('b', 'b', 'A', 200)},
        {'a': Category3Demo('a', 'a', 'A', 200),
         'b': Category3Demo('b', 'b', 'A', 200),
         'c': Category3Demo('c', 'c', 'A', 200),
         'd': Category3Demo('d', 'd', 'A', 200),
         'e': Category3Demo('e', 'e', 'A', 200),
         'f': Category3Demo('f', 'f', 'A', 200),
         'g': Category3Demo('g', 'g', 'A', 200)},
        {'a': Category3Demo('a', 'a', 'A', 200),
         'b': Category3Demo('b', 'b', 'A', 200),
         'c': Category3Demo('c', 'c', 'A', 200),
         'd': Category3Demo('d', 'd', 'A', 200),
         'e': Category3Demo('e', 'e', 'A', 200),
         'f': Category3Demo('f', 'f', 'A', 200),
         'g': Category3Demo('g', 'g', 'A', 200)
         },
        {'a': Category3Demo('a', 'a', 'A', 200),
         'b': Category3Demo('b', 'b', 'A', 200),
         'c': Category3Demo('c', 'c', 'A', 200),
         'd': Category3Demo('d', 'd', 'A', 200),
         'f': Category3Demo('f', 'f', 'A', 200)
         },
        {'a': Category3Demo('a', 'a', 'A', 200),
         'b': Category3Demo('b', 'b', 'A', 200),
         'c': Category3Demo('c', 'c', 'A', 200),
         'd': Category3Demo('d', 'd', 'A', 200),
         'e': Category3Demo('e', 'e', 'A', 200),
         'f': Category3Demo('f', 'f', 'A', 200),
         'g': Category3Demo('g', 'g', 'A', 200),
         'h': Category3Demo('h', 'h', 'A', 200),
         'i': Category3Demo('i', 'i', 'A', 200),
         'j': Category3Demo('j', 'j', 'A', 200),
         'k': Category3Demo('k', 'k', 'A', 200),
         'l': Category3Demo('l', 'l', 'A', 200),
         'm': Category3Demo('m', 'm', 'A', 200),
         'bi': Category3Demo('bi', 'bi', 'B', 200),
         'bj': Category3Demo('bj', 'bj', 'B', 200),
         'bk': Category3Demo('bk', 'bk', 'B', 200)},
    ]

    n = 6
    a = main_calculate(category3_to_category3_obj[n], category3_intimate_weight[n], category3_level_value[n])
    print('--------------候选列表---------------')
    print('候选列表总数：', len(a))
    print(a)
