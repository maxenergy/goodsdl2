import logging
from dl.utils import visualization_utils as vis_util
import numpy as np
from sklearn.cluster import KMeans
import traceback
logger = logging.getLogger("django")

def get_client_ip(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip

def get_host_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

def visualize_boxes_and_labels_on_image_array_V2(image,
                                                 boxes,
                                                 upcs,
                                                 scores_step1,
                                                 scores_step2,
                                                 instance_masks=None,
                                                 keypoints=None,
                                                 use_normalized_coordinates=False,
                                                 max_boxes_to_draw=50,
                                                 step1_min_score_thresh=.0,
                                                 step2_min_score_thresh=.5,
                                                 agnostic_mode=False,
                                                 line_thickness=4):
    """Overlay labeled boxes on an image with formatted scores and label names.

    This function groups boxes that correspond to the same location
    and creates a display string for each detection and overlays these
    on the image. Note that this function modifies the image in place, and returns
    that same image.

    Args:
      image: uint8 numpy array with shape (img_height, img_width, 3)
      boxes: a numpy array of shape [N, 4]
      upcs: a numpy array of shape [N]. Note that class indices are 1-based,
        and match the keys in the label map.
      scores_step1: a numpy array of shape [N] or None.  If scores=None, then
        this function assumes that the boxes to be plotted are groundtruth
        boxes and plot all boxes as black with no classes or scores.
      instance_masks: a numpy array of shape [N, image_height, image_width], can
        be None
      keypoints: a numpy array of shape [N, num_keypoints, 2], can
        be None
      use_normalized_coordinates: whether boxes is to be interpreted as
        normalized coordinates or not.
      max_boxes_to_draw: maximum number of boxes to visualize.  If None, draw
        all boxes.
      step1_min_score_thresh: step1 minimum score threshold for a box to be visualized
      step2_min_score_thresh: step2 minimum score a bounding box's color
      agnostic_mode: boolean (default: False) controlling whether to evaluate in
        class-agnostic mode or not.  This mode will display scores but ignore
        classes.
      line_thickness: integer (default: 4) controlling line width of the boxes.

    Returns:
      uint8 numpy array with shape (img_height, img_width, 3) with overlaid boxes.
    """
    # Create a display string (and color) for every box location, group any boxes
    # that correspond to the same location.
    box_to_display_str_map = vis_util.collections.defaultdict(list)
    box_to_color_map = vis_util.collections.defaultdict(str)
    box_to_instance_masks_map = {}
    box_to_keypoints_map = vis_util.collections.defaultdict(list)
    if not max_boxes_to_draw:
        max_boxes_to_draw = boxes.shape[0]
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores_step1 is None or scores_step1[i] > step1_min_score_thresh:
            box = tuple(boxes[i].tolist())
            if instance_masks is not None:
                box_to_instance_masks_map[box] = instance_masks[i]
            if keypoints is not None:
                box_to_keypoints_map[box].extend(keypoints[i])
            if scores_step1 is None:
                box_to_color_map[box] = 'black'
            else:
                if not agnostic_mode:
                    class_name = upcs[i]
                    display_str = '{}'.format(class_name)
                    box_to_display_str_map[box].append(display_str)
                    display_str = '{}%, {}%'.format(
                        int(100 * scores_step1[i]),
                        int(100 * scores_step2[i]),
                    )
                    box_to_display_str_map[box].append(display_str)
                else:
                    display_str = 'score: {}%, {}%'.format(int(100 * scores_step1[i]),
                                                           int(100 * scores_step2[i]))
                    box_to_display_str_map[box].append(display_str)
                if agnostic_mode:
                    box_to_color_map[box] = 'DarkOrange'
                else:
                    if scores_step2[i] < step2_min_score_thresh:
                        box_to_color_map[box] = 'Red'
                    else:
                        box_to_color_map[box] = 'DarkOrange'

    # Draw all boxes onto image.
    for box, color in box_to_color_map.items():
        ymin, xmin, ymax, xmax = box
        if instance_masks is not None:
            vis_util.draw_mask_on_image_array(
                image,
                box_to_instance_masks_map[box],
                color=color
            )
        vis_util.draw_bounding_box_on_image_array(
            image,
            ymin,
            xmin,
            ymax,
            xmax,
            color=color,
            thickness=line_thickness,
            display_str_list=box_to_display_str_map[box],
            use_normalized_coordinates=use_normalized_coordinates)
        if keypoints is not None:
            vis_util.draw_keypoints_on_image_array(
                image,
                box_to_keypoints_map[box],
                color=color,
                radius=line_thickness / 2,
                use_normalized_coordinates=use_normalized_coordinates)

    return image

def visualize_boxes_and_labels_on_image_array_V1(image,
                                              boxes,
                                              scores_step1,
                                              instance_masks=None,
                                              keypoints=None,
                                              use_normalized_coordinates=False,
                                              max_boxes_to_draw=50,
                                              step1_min_score_thresh=.5,
                                              line_thickness=4,
                                              show_error_boxes = True):
    """Overlay labeled boxes on an image with formatted scores and label names.

    This function groups boxes that correspond to the same location
    and creates a display string for each detection and overlays these
    on the image. Note that this function modifies the image in place, and returns
    that same image.

    Args:
      image: uint8 numpy array with shape (img_height, img_width, 3)
      boxes: a numpy array of shape [N, 4]
      scores_step1: a numpy array of shape [N] or None.  If scores=None, then
        this function assumes that the boxes to be plotted are groundtruth
        boxes and plot all boxes as black with no classes or scores.
      instance_masks: a numpy array of shape [N, image_height, image_width], can
        be None
      keypoints: a numpy array of shape [N, num_keypoints, 2], can
        be None
      use_normalized_coordinates: whether boxes is to be interpreted as
        normalized coordinates or not.
      max_boxes_to_draw: maximum number of boxes to visualize.  If None, draw
        all boxes.
      step1_min_score_thresh: step1 minimum score threshold for a box to be visualized
      line_thickness: integer (default: 4) controlling line width of the boxes.

    Returns:
      uint8 numpy array with shape (img_height, img_width, 3) with overlaid boxes.
    """
    # Create a display string (and color) for every box location, group any boxes
    # that correspond to the same location.
    box_to_display_str_map = vis_util.collections.defaultdict(list)
    box_to_color_map = vis_util.collections.defaultdict(str)
    box_to_instance_masks_map = {}
    box_to_keypoints_map = vis_util.collections.defaultdict(list)
    if not max_boxes_to_draw:
        max_boxes_to_draw = boxes.shape[0]
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores_step1 is None or scores_step1[i] > 0.01:
            if scores_step1[i] >= step1_min_score_thresh or show_error_boxes:
                box = tuple(boxes[i].tolist())
                if instance_masks is not None:
                    box_to_instance_masks_map[box] = instance_masks[i]
                if keypoints is not None:
                    box_to_keypoints_map[box].extend(keypoints[i])
                if scores_step1 is None:
                    box_to_color_map[box] = 'black'
                else:
                    display_str = '{}%'.format(int(100 * scores_step1[i]),)
                    box_to_display_str_map[box].append(display_str)
                    if scores_step1[i] > step1_min_score_thresh:
                        box_to_color_map[box] = 'RoyalBlue'
                    else:
                        box_to_color_map[box] = 'Red'

    # Draw all boxes onto image.
    for box, color in box_to_color_map.items():
        ymin, xmin, ymax, xmax = box
        if instance_masks is not None:
            vis_util.draw_mask_on_image_array(
                image,
                box_to_instance_masks_map[box],
                color=color
            )
        vis_util.draw_bounding_box_on_image_array(
            image,
            ymin,
            xmin,
            ymax,
            xmax,
            color=color,
            thickness=line_thickness,
            display_str_list=box_to_display_str_map[box],
            use_normalized_coordinates=use_normalized_coordinates)
        if keypoints is not None:
            vis_util.draw_keypoints_on_image_array(
                image,
                box_to_keypoints_map[box],
                color=color,
                radius=line_thickness / 2,
                use_normalized_coordinates=use_normalized_coordinates)

    return image


def visualize_boxes_and_labels_on_image_array_for_shelf(image,
                                                        boxes,
                                                        text_infos,
                                                        color_infos,
                                                        line_thickness=4):
    """Overlay labeled boxes on an image with formatted scores and label names.

    This function groups boxes that correspond to the same location
    and creates a display string for each detection and overlays these
    on the image. Note that this function modifies the image in place, and returns
    that same image.

    Args:
      image: uint8 numpy array with shape (img_height, img_width, 3)
      boxes: a numpy array of shape [N, 4]
      text_infos: a python array of text_info
      color_infos: a python array of color_info
      line_thickness: integer (default: 4) controlling line width of the boxes.

    Returns:
      uint8 numpy array with shape (img_height, img_width, 3) with overlaid boxes.
    """
    # Create a display string (and color) for every box location, group any boxes
    # that correspond to the same location.
    box_to_display_str_map = vis_util.collections.defaultdict(list)
    box_to_color_map = vis_util.collections.defaultdict(str)
    for i in range(len(boxes)):
        box = boxes[i]
        ymin = box['ymin']
        xmin = box['xmin']
        ymax = box['ymax']
        xmax = box['xmax']
        color = color_infos[i]
        vis_util.draw_bounding_box_on_image_array(
            image,
            ymin,
            xmin,
            ymax,
            xmax,
            color=color,
            thickness=line_thickness,
            display_str_list=[text_infos[i]],
            use_normalized_coordinates=False)

    return image


def caculate_level(boxes, n_clusters=6):
    """
    通过连续聚类计算框所属的层级
    @param boxes 这是一个数组对象，数组中每个对象是个字典，字典中有都有ymin和ymax字段，计算完字典中加入level字段
    """
    try:
        data = []
        for one_box in boxes:
            data.append((one_box['ymin'], one_box['ymax']))
        X = np.array(data)
        estimator = KMeans(n_clusters=int(n_clusters))
        estimator.fit(X)
        label_pred = estimator.labels_  # 获取聚类标签
        label_to_mean = {}

        for i in range(n_clusters):
            one_X = X[label_pred == i]
            label_to_mean[i] = np.sum(one_X) / one_X.shape[0]

        # 根据平均值排序
        sorted_list = sorted(label_to_mean.items(), key=lambda item: item[1])
        t = np.array(sorted_list, dtype=int)
        t = t[:, 0]
        sorted_label = {}
        for i in range(t.shape[0]):
            sorted_label[t[i]] = i

        for i in range(len(boxes)):
            box_label = label_pred[i]
            boxes[i]['level'] = sorted_label[box_label]
    except Exception as e:
        logger.error('caculate level error:{}'.format(e))
        traceback.print_exc()