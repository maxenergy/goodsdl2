get_display_good="select display_goods_info from sf_taizhang_display where id=%d and start_datetime is not null and end_datetime is not null and now() > start_datetime and now() <= end_datetime"
