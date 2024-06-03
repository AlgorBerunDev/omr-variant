import cv2
import numpy as np

def find_intersection_area(image, contour1, contour2):
    """
    Функция для нахождения области пересечения двух контуров.

    :param image: Входное изображение.
    :param contour1: Первый контур.
    :param contour2: Второй контур.
    :return: Область пересечения (если есть) или None.
    """
    # Получаем размеры изображения
    height, width = image.shape[:2]

    # Создаем пустые изображения для контуров
    img1 = np.zeros((height, width), dtype=np.uint8)
    img2 = np.zeros((height, width), dtype=np.uint8)

    # Рисуем контуры на изображениях
    cv2.drawContours(img1, [contour1], -1, 255, -1)
    cv2.drawContours(img2, [contour2], -1, 255, -1)

    # Находим пересечение двух изображений
    intersection = cv2.bitwise_and(img1, img2)

    # Находим контуры пересечения
    contours, _ = cv2.findContours(intersection, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Вычисляем области пересечения
        intersection_areas = [cv2.contourArea(c) for c in contours]
        return intersection_areas
    else:
        return None

def check_cross(cnt1, cnt2, percent_cross_of_cnt1, percent_cross_of_cnt2):
  return False

def remove_cross(cnts1, cnts2, great_then_percent_cross_of_cnt1, great_then_percent_cross_of_cnt2):
  return False 
