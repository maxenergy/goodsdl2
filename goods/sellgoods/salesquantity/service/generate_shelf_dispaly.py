import os
import cv2
import numpy as np
import json
from set_config import config
from goods.sellgoods.salesquantity.local_util import shelf_display
from goods.sellgoods.commonbean.taizhang import Taizhang
from goods.sellgoods.commonbean.shelf import Shelf
from goods.sellgoods.commonbean.good import Good
from goods.goodsdata import get_raw_shop_shelfs,get_raw_goods_info
from goods.sellgoods.auto_choose_goods.out_service_api import goods_sort,calculate_goods_info
# 生成自动陈列
# shelf_display = config.shellgoods_params['shelf_display']

def generate_displays(uc_shopid, tz_id):
    """
    :param uc_shopid:
    :param tz_id:
    :return:
    """

    taizhang = Taizhang()
    # 生成taizhang对象，初始化所有数据相关的字段
    raw_shelfs = get_raw_shop_shelfs(uc_shopid,tz_id)
    if raw_shelfs is None or len(raw_shelfs)==0:
        raise ValueError('not found shelf!')
    taizhang.tz_id = tz_id
    for raw_shelf in raw_shelfs:
        shelf = Shelf(
            raw_shelf.taizhang_id,
            raw_shelf.shelf_id,
            raw_shelf.length,
            raw_shelf.height,
            raw_shelf.depth,
            raw_shelf.hole_height,
            raw_shelf.hole_dis
        )
        taizhang.associated_catids = raw_shelf.associated_catids
        taizhang.shelfs.append(shelf)

    # caculate_goods_array 李树、华超
    simple_goods_list = goods_sort(taizhang.associated_catids)
    mch_codes = []
    for simple_goods in simple_goods_list:
        mch_codes.append(simple_goods[0])

    # 李树：输入参数中类的list，mch_goods_code列表，返回一个mch_goods_code列表
    # 华超：根据上一步生成caculate_goods_array，将所有goods的数据信息填入
    mch_codes_to_data_raw_goods = get_raw_goods_info(uc_shopid,mch_codes)
    taizhang.calculate_goods_array = []
    for simple_goods in simple_goods_list:
        if simple_goods[0] in mch_codes_to_data_raw_goods:
            data_raw_goods = mch_codes_to_data_raw_goods[simple_goods[0]]
            good = Good()
            good.mch_good_code = simple_goods[0]
            good.sale_account = simple_goods[1]
            corp_classify_code = data_raw_goods.corp_classify_code
            if len(str(corp_classify_code)) == 6:
                good.first_cls_code = corp_classify_code[0:2]
                good.second_cls_code = corp_classify_code[0:4]
                good.third_cls_code = corp_classify_code
            else:
                good.first_cls_code = 0
                good.second_cls_code = 0
                good.third_cls_code = 0
                print('corp_classify_code error: {}'.format(corp_classify_code))

            # 陈列分类code TODO
            if len(str(data_raw_goods.display_code)) == 6:
                good.display_code = data_raw_goods.display_code
            else:
                good.display_code = 0
                print('corp_classify_code error: {}'.format(corp_classify_code))

            good.name = data_raw_goods.goods_name
            good.upc = data_raw_goods.upc
            good.icon = data_raw_goods.tz_display_img
            good.width = data_raw_goods.width
            good.height = data_raw_goods.height
            good.depth = data_raw_goods.depth
            good.start_num = data_raw_goods.start_sum
            good.fitting_rows = 1 # 需要挂放几行
            good.is_superimpose = data_raw_goods.is_superimpose
            good.isfitting = data_raw_goods.is_suspension
            good.superimpose_rows = 2 # 叠放几行
            taizhang.calculate_goods_array.append(good)

    # twidth_to_goods 李树
    # 输入：taizhang，
    # 将goods的计算信息填入，同时将twidth_to_goods生成出来
    calculate_goods_info(taizhang)

    # 排列货架 生成陈列
    shelf_display.generate(taizhang)

    return taizhang

def print_taizhang(taizhang,image_dir):
    import urllib.request
    from django.conf import settings
    index = 0

    # import PIL.ImageFont as ImageFont
    #     fontText = ImageFont.truetype("font/simsun.ttc", 12, encoding="utf-8")

    picurl_to_goods_image = {}
    for shelf in taizhang.shelfs:
        index += 1
        image_path = os.path.join(image_dir,'{}.jpg'.format(index))
        image = np.ones((shelf.height,shelf.width,3),dtype=np.int16)
        image = image*255

        for level in shelf.levels:
            if level.isTrue:
                level_start_height = level.level_start_height
                for good in level.goods:
                    picurl = '{}{}'.format(settings.UC_PIC_HOST, good.icon)
                    if picurl in picurl_to_goods_image:
                        goods_image = picurl_to_goods_image[picurl]
                    else:
                        try:
                            goods_image_name = '{}.jpg'.format(good.mch_good_code)
                            goods_image_path = os.path.join(image_dir, goods_image_name)
                            urllib.request.urlretrieve(picurl, goods_image_path)
                            goods_image = cv2.imread(goods_image_path)
                            goods_image = cv2.resize(goods_image,(good.width,good.height))
                        except Exception as e:
                            print('get goods pic error:{}'.format(e))
                            goods_image = None
                        picurl_to_goods_image[picurl] = goods_image

                    for gooddisplay in good.gooddisplay_inss:
                        if gooddisplay.dep == 0:
                            point1 = (gooddisplay.left,shelf.height-(gooddisplay.top+level_start_height+good.height))
                            point2 = (gooddisplay.left+good.width,shelf.height-(gooddisplay.top+level_start_height))
                            cv2.rectangle(image, point1, point2, (0, 0, 255), 2)
                            # if goods_image is None:
                            #     cv2.rectangle(image,point1,point2,(0,0,255),2)
                            # else:
                            #     h = goods_image.shape[0]
                            #     w = goods_image.shape[1]
                            #     image[point1[1]:point1[1]+h, point1[0]:point1[0]+w,:] = goods_image
                            txt_point = (gooddisplay.left,shelf.height-(gooddisplay.top+level_start_height+int(good.height/2)))
                            cv2.putText(image, '{}'.format(good.mch_good_code),txt_point, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        cv2.imwrite(image_path,image)

if __name__ == "__main__":
    taizhang = generate_displays(806,1142)
    print(json.dumps(taizhang.to_json()))
    import os
    with open("1.txt","w") as f:
        f.write(str(taizhang.__str__()))
    image_dir = '/home/src/goodsdl2/media/images/taizhang/{}'.format(taizhang.tz_id)
    from pathlib import Path
    if not Path(image_dir).exists():
        os.makedirs(image_dir)
    print_taizhang(taizhang, image_dir)
