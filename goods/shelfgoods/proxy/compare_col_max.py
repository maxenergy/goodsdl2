from goods.shelfgoods.bean import code
from dl import shelftradition_match
import logging
logger = logging.getLogger("detect")
from set_config import config
from goods.shelfgoods.imgsearch.aliyun.search import ImgSearch
aliyun_search_img_switch = config.common_params['aliyun_search_img_switch']
def process(check_box_ins,display_ins,shelf_img,with_in_upcs=None):
    logger.info("level proxy process is compare_col_max ..................")
    ck_goodscolumn_inss = check_box_ins.gbx_ins.goodscolumns
    ds_goodscolumn_inss = display_ins.gbx_ins.goodscolumns
    ck_cols = check_box_ins.gbx_ins.level_columns
    ds_cols = display_ins.gbx_ins.level_columns
    col_goods={}
    logger.info("level proxy process is compare_col_min  ck_cols=%s,ds_cols =%s" % (str(ck_cols), str(ds_cols)))
    col_compare_l = {}
    ck_goodscolumn_inss_copys = {}
    for i in range(ck_cols-ds_cols+1):
        ck_goodscolumn_inss_copy = ck_goodscolumn_inss.copy()
        ds_goodscolumn_inss_copy = ds_goodscolumn_inss.copy()
        sum_model_true,col_l,ck_goodscolumn_inss_copy = sum_compare_model_true(ck_goodscolumn_inss_copy,ds_goodscolumn_inss_copy,i,shelf_img)
        col_goods[i] = sum_model_true
        col_compare_l[i] = col_l
        ck_goodscolumn_inss_copys[i] = ck_goodscolumn_inss_copy
    a = sorted(col_goods.items(), key=lambda x: x[1], reverse=True)
    col_good_i = a[0][0]
    logger.info("level proxy process is compare_col_max  col_good_i = "+str(col_good_i))
    logger.info("col_compare_l[col_good_i]:" + str(col_compare_l[col_good_i]))
    check_box_ins = process_good_col(check_box_ins,col_compare_l[col_good_i],ck_goodscolumn_inss_copys[col_good_i])
    return check_box_ins, display_ins

def process_good_col(check_box_ins,col_compare_l,ck_goodscolumn_inss_copy):
    ck_goodscolumn_inss = check_box_ins.gbx_ins.goodscolumns
    for ck_gcs,ck_gcs_copy in zip(ck_goodscolumn_inss,ck_goodscolumn_inss_copy):
        if ck_gcs == [] or ck_gcs == None :
            continue
        ck_location_column = ck_gcs.location_column
        ck_location_row = ck_gcs.location_row
        ck_box = ck_gcs.location_box
        for i in range(len(col_compare_l)):
            (col,row,result) = col_compare_l[i]
            if ck_gcs.compare_code == None and ck_location_column==col and ck_location_row==row:
                ck_gcs.compare_code=code.match_result[result]
                ck_gcs.compare_result = code.result_code[ck_gcs.compare_code]
                ck_gcs.upc = ck_gcs_copy.upc

    for ck_gcs in ck_goodscolumn_inss:
        if ck_gcs == [] or ck_gcs == None :
            continue
        if ck_gcs.compare_code==None:
            ck_gcs.compare_code=code.code_8
            ck_gcs.compare_result = code.result_code[ck_gcs.compare_code]
    return check_box_ins


def sum_compare_model_true(ck_goodscolumn_inss,ds_goodscolumn_inss,i,shelf_img):
    sum_true = 0
    compare_re_l=[]
    for ds_gcs in ds_goodscolumn_inss:
    # for ck_gcs in ck_goodscolumn_inss:
        if ds_gcs == [] or ds_gcs == None:
            continue
        ds_upc = ds_gcs.upc
        ds_location_column = ds_gcs.location_column
        ds_location_row = ds_gcs.location_row
        # logger.info(
        # "ds_location_column,ds_location_row=(%s,%s)" % (str(ds_location_column), str(ds_location_row)))
        # ds_rows = get_col_display_max(ds_goodscolumn_inss, ds_location_column)
        # if len(ds_rows) > 0:
        for ck_gcs in ck_goodscolumn_inss:
            if ck_gcs == [] or ck_gcs == None:
                continue
            if ck_gcs.is_label is not None and ck_gcs.is_label == 1:  # 人工已标注的不做比对
                continue
            ck_location_column = ck_gcs.location_column - i
            ck_location_row = ck_gcs.location_row
            # logger.info(
            #     "ck_location_column,ck_location_row=(%s,%s)" % (str(ck_location_column), str(ck_location_row)))
            ck_box = ck_gcs.location_box
            # compare_result = ck_gcs.compare_result
            # compare_code = ck_gcs.compare_code
            if ck_gcs.compare_code == None and ds_location_column == ck_location_column and ds_location_row == ck_location_row:
                logger.info("(box_id,xmin,ymin,xmax,ymax)=(%s,%s,%s,%s,%s)" % (str(ck_gcs.box_id),str(ck_box[0]), str(ck_box[1]), str(ck_box[2]), str(ck_box[3])))
                target_img = shelf_img[int(ck_box[1]):int(ck_box[3]), int(ck_box[0]):int(ck_box[2])]
                if aliyun_search_img_switch:
                    search_ins = ImgSearch()
                    upcs = search_ins.search_cvimg(target_img)
                    logger.info("ck_box box_id=%s,upc=%s,aliyun match upc=%s,ds=(%s,%s),ck=(%s,%s)" % (
                    str(ck_gcs.box_id), str(ds_upc), str(upcs), str(ds_location_column), str(ds_location_row),
                    str(ck_location_column), str(ck_location_row)))
                    if upcs != None and len(upcs) > 0 and ds_upc in upcs:
                        ck_gcs.compare_code = code.code_12
                        ck_gcs.compare_result = code.result_code[ck_gcs.compare_code]
                        ck_gcs.upc = ds_upc
                        sum_true += 1
                    elif (upcs != None and len(upcs) > 0 and ds_upc not in upcs):
                        ck_gcs.compare_code = code.code_13
                        ck_gcs.compare_result = code.result_code[ck_gcs.compare_code]
                    elif (upcs != None and len(upcs) <= 0):
                        ck_gcs.compare_code = code.code_14
                        ck_gcs.compare_result = code.result_code[ck_gcs.compare_code]
                    else:
                        ck_gcs.compare_code = code.code_15
                        ck_gcs.compare_result = code.result_code[ck_gcs.compare_code]
                    break
                else:
                    match_ins = shelftradition_match.ShelfTraditionMatch(ds_upc)
                    match_result = match_ins.detect_one_with_cv2array(target_img)
                    logger.info("ck_box box_id=%s,upc=%s,match_result=%s,ds=(%s,%s),ck=(%s,%s)" % (
                    str(ck_gcs.box_id), str(ds_upc), str(code.match_result[match_result]),str(ds_location_column), str(ds_location_row),str(ck_location_column),str(ck_location_row)))
                    compare_re_l.append((ck_location_column,ck_location_row,match_result))
                    if  match_result == True:
                        ck_gcs.upc = ds_upc
                        sum_true+=1
                    break
            else:
                continue
    return sum_true,compare_re_l,ck_goodscolumn_inss


def get_col_display_max(ds_goodscolumn_inss,col):
    rows = []
    for ds_gcs in ds_goodscolumn_inss:
        ds_upc = ds_gcs.upc
        ds_location_column = ds_gcs.location_column
        ds_location_row = ds_gcs.location_row
        if col == ds_location_column:
            rows.append(ds_location_row)
    return rows
