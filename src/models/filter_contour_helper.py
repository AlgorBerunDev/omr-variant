import cv2


def get_counters_after_counter(counters, counter, axis='y'):
    """
    Возвращает контуры, находящиеся после заданного контура вдоль указанной оси.
    
    :param counters: Список контуров.
    :param counter: Заданный контур.
    :param axis: Ось ('x' или 'y'), вдоль которой проверяется положение контуров.
    :return: Список контуров, находящихся после заданного контура вдоль указанной оси.
    """
    # Определяем координаты заданного контура вдоль указанной оси
    if axis == 'y':
        _, y, _, h = cv2.boundingRect(counter)
        threshold = y + h
    elif axis == 'x':
        x, _, w, _ = cv2.boundingRect(counter)
        threshold = x + w
    else:
        raise ValueError("Invalid axis. Use 'x' or 'y'.")
    
    # Отфильтровываем контуры, которые находятся после заданного контура вдоль указанной оси
    result = []
    for cnt in counters:
        if axis == 'y':
            _, y, _, _ = cv2.boundingRect(cnt)
            if y > threshold:
                result.append(cnt)
        elif axis == 'x':
            x, _, _, _ = cv2.boundingRect(cnt)
            if x > threshold:
                result.append(cnt)
    
    return result

def get_counters_before_counter(counters, counter, axis='y'):
    """
    Возвращает контуры, находящиеся перед заданным контуром вдоль указанной оси.
    
    :param counters: Список контуров.
    :param counter: Заданный контур.
    :param axis: Ось ('x' или 'y'), вдоль которой проверяется положение контуров.
    :return: Список контуров, находящихся перед заданным контуром вдоль указанной оси.
    """
    # Определяем координаты заданного контура вдоль указанной оси
    if axis == 'y':
        _, y, _, _ = cv2.boundingRect(counter)
        threshold = y
    elif axis == 'x':
        x, _, _, _ = cv2.boundingRect(counter)
        threshold = x
    else:
        raise ValueError("Invalid axis. Use 'x' or 'y'.")
    
    # Отфильтровываем контуры, которые находятся перед заданным контуром вдоль указанной оси
    result = []
    for cnt in counters:
        if axis == 'y':
            _, y, _, _ = cv2.boundingRect(cnt)
            if y < threshold:
                result.append(cnt)
        elif axis == 'x':
            x, _, _, _ = cv2.boundingRect(cnt)
            if x < threshold:
                result.append(cnt)
    
    return result

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

def find_contour_by_y_order(contours, order=1):
    contours.sort(key=lambda contour: cv2.boundingRect(contour)[1])

    # Возвращаем контур по порядковому номеру
    if 0 < order <= len(contours):
        return contours[order - 1]
    else:
        return None

