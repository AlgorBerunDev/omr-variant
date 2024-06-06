import cv2
from intersection_functions import is_intersects

def get_gt_n_intersect_counters(contours, gt_n = 65, axis='x'):
    """
    Berilan axis bo'yicha gt_n martadan ortiq kesishgan konturlarni qaytaradi

    :param counters: Konturlar
    :param gt_n: axis bo'yicha kesishishlar soni
    :return: axis bo'yicha N marta kesishgan konturlar
    """
    gt_n_intersection_cnts = []
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        intersection_count = 0
        for cnt1 in contours:
            x1,y1,w1,h1 = cv2.boundingRect(cnt1)
            if axis == 'x':
                if is_intersects(x,w,x1,w1):
                    intersection_count = intersection_count + 1
            elif axis == 'y':
                if is_intersects(y,h,y1,h1):
                    intersection_count = intersection_count + 1
        if intersection_count >= gt_n:
            gt_n_intersection_cnts.append(cnt)
    return gt_n_intersection_cnts

def filter_by_aspect_ratio(contours, min_aspect_ration = 1, max_aspect_ratio = 7):
    filtered_contours = []
    # Проход по всем найденным контурам
    for contour in contours:
        # Вычисление ограничивающего прямоугольника для каждого контура
        x, y, w, h = cv2.boundingRect(contour)
    
        # Проверка соотношений сторон
        if min_aspect_ration < w / h < max_aspect_ratio :
            filtered_contours.append(contour)
    return filtered_contours

def filter_by_area_ratio(contours, min_area_ratio = 0.4, max_area_ratio=2.5, min_area_ratio_suitable_count = 40):
    filtered_counters = []
    for cnt in contours:
        area_ratio_suitable_count = 0
        cnt_area = cv2.contourArea(cnt)
        for cnt1 in contours:
            cnt1_area = cv2.contourArea(cnt1)
            if cnt1_area != 0 and min_area_ratio <= float(cnt_area) / cnt1_area <= max_area_ratio:
                area_ratio_suitable_count = area_ratio_suitable_count + 1
        if area_ratio_suitable_count >= min_area_ratio_suitable_count:
            filtered_counters.append(cnt)
    return filtered_counters
