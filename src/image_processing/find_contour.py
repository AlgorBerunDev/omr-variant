import cv2
import numpy as np
from filter_functions import filter_by_area_ratio, filter_by_aspect_ratio, get_gt_n_intersect_counters

def find_contour_by_y_order(contours, order=1):
    contours.sort(key=lambda contour: cv2.boundingRect(contour)[1])

    # Возвращаем контур по порядковому номеру
    if 0 < order <= len(contours):
        return contours[order - 1]
    else:
        return None

def find_contours_of_base_rectangles(image, threshold_value = 100, num_contours = 65):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blurred = cv2.GaussianBlur(gray, (3,3), 0)

    # Применение эрозии для улучшения видимости контуров
    kernel = np.ones((1,1), np.uint8)
    eroded = cv2.erode(gray, kernel, iterations=1)


    # Применение порогового значения для выделения объектов
    _, binary = cv2.threshold(eroded, threshold_value, 255, cv2.THRESH_BINARY_INV)

    # Поиск контуров
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Список для хранения подходящих контуров
    filtered_contours = filter_by_aspect_ratio(contours)
    filtered_contours = get_gt_n_intersect_counters(filtered_contours, 60)
    filtered_contours = filter_by_area_ratio(filtered_contours)



    # Сортировка контуров по координате x (самые левые)
    filtered_contours.sort(key=lambda contour: cv2.boundingRect(contour)[0])

    # Оставляем только самые левые num_contours контуров
    return filtered_contours[:num_contours]

