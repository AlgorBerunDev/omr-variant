import cv2
import numpy as np

def check_intersection(contour1, contour2):
    """
    Проверяет пересечение двух контуров.
    
    :param contour1: Первый контур.
    :param contour2: Второй контур.
    :return: True, если есть пересечение, иначе False.
    """
    if len(contour1) == 0 or len(contour2) == 0:
        return False
    
    # Преобразуем контуры в выпуклые оболочки
    hull1 = cv2.convexHull(contour1.astype(np.float32))
    hull2 = cv2.convexHull(contour2.astype(np.float32))
    
    # Проверка пересечения выпуклых оболочек
    ret, _ = cv2.intersectConvexConvex(hull1, hull2)
    
    return ret > 0


def intersection_area(contour1, contour2):
    """
    Вычисляет площадь пересечения двух контуров.
    
    :param contour1: Первый контур.
    :param contour2: Второй контур.
    :return: Площадь пересечения.
    """
    # Создаем пустое изображение
    img = np.zeros((1000, 1000), dtype=np.uint8)
    
    # Рисуем первый контур
    cv2.fillPoly(img, [contour1.astype(np.int32)], 1)
    
    # Рисуем второй контур
    cv2.fillPoly(img, [contour2.astype(np.int32)], 1)
    
    # Считаем количество пересечений
    intersection = np.sum(img == 2)
    
    return intersection

def find_intersections(leftmost_contours, circle_contours):
    intersections = []
    
    for left_contour in leftmost_contours:
        for circle_contour in circle_contours:
            if check_intersection(left_contour, circle_contour):
                intersections.append(left_contour)
                break

    return intersections

def remove_intersections(counters, filter_counters):
  not_intersections = []
    
  for counter in counters:
    is_intersection = False
    for filter_counter in filter_counters:
        if check_intersection(counter, filter_counter):
            is_intersection = True
            break
    if not is_intersection:
      not_intersections.append(counter)
  return not_intersections

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

def create_horizontal_rectangle_counter(counter, max_width_point):
    """
    Создает горизонтальный контур (прямоугольник) на основе заданного контура.
    
    :param counter: Заданный контур.
    :param max_width_point: Максимальная точка по ширине.
    :return: Горизонтальный контур (прямоугольник).
    """
    if len(counter) == 0:
        return np.array([], dtype=np.float32)
    
    # Определяем ограничивающий прямоугольник для контура
    x, y, w, h = cv2.boundingRect(counter)
    
    # Создаем горизонтальный контур (прямоугольник)
    horizontal_rectangle_counter = np.array([[x, y], [max_width_point, y], [max_width_point, y + h], [x, y + h]], dtype=np.float32)
    
    return horizontal_rectangle_counter

def intersection_length(line1_start_x, line1_end_x, line2_start_x, line2_end_x):
    # Убедимся, что координаты отрезков упорядочены
    if line1_start_x > line1_end_x:
        line1_start_x, line1_end_x = line1_end_x, line1_start_x
    if line2_start_x > line2_end_x:
        line2_start_x, line2_end_x = line2_end_x, line2_start_x
    
    # Найдём координаты начала и конца пересечения
    start = max(line1_start_x, line2_start_x)
    end = min(line1_end_x, line2_end_x)
    
    # Вычислим длину пересечения
    length = max(0, end - start)
    
    return length
