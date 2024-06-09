import cv2
import numpy as np

class IntersectionHelper:
  def check_intersection(contour1, contour2):
    """
    Проверяет пересечение двух контуров.

    :param contour1: Первый контур.
    :param contour2: Второй контур.
    :return: True, если есть пересечение, иначе False.
    """
    if contour1 is None or contour2 is None:
        return False

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

  def find_intersections(self, leftmost_contours, circle_contours):
    intersections = []

    for left_contour in leftmost_contours:
        for circle_contour in circle_contours:
            if self.check_intersection(left_contour, circle_contour):
                intersections.append(left_contour)
                break

    return intersections
  
  def remove_intersections(self, counters, filter_counters):
    not_intersections = []

    for counter in counters:
        is_intersection = False
        for filter_counter in filter_counters:
            if self.check_intersection(counter, filter_counter):
                is_intersection = True
                break
        if not is_intersection:
            not_intersections.append(counter)
    return not_intersections
  
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
  
  def is_intersects(x1, w1, x2, w2):
    return (x1 <= x2 <= x1 + w1) or (x2 <= x1 <= x2 + w2)
  
  def group_by_intersection_by_axis(self, counters, axis = 'x'):
    intersection_groups = []

    for cnt1 in counters:
        x1,y1,w1,h1 = cv2.boundingRect(cnt1)
        for cnt2 in counters:
            x2,y2,w2,h2 = cv2.boundingRect(cnt2)
            if axis == 'x':
                if self.is_intersects(x1, w1, x2, w2):
                    intersection_groups.append(cnt2)
            elif axis == 'y':
                if self.is_intersects(x1, w1, x2, w2):
                    intersection_groups.append(cnt2)

    return intersection_groups
  
  def get_gt_n_intersect_counters(self, contours, gt_n = 65, axis='x'):
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
                if self.is_intersects(x,w,x1,w1):
                    intersection_count = intersection_count + 1
            elif axis == 'y':
                if self.is_intersects(y,h,y1,h1):
                    intersection_count = intersection_count + 1
        if intersection_count >= gt_n:
            gt_n_intersection_cnts.append(cnt)
    return gt_n_intersection_cnts
