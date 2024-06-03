import cv2
import numpy as np
import math
from left_counters import find_contour_by_y_order, find_left_counters
from intersection_functions import remove_intersections, get_counters_after_counter, get_counters_before_counter, intersection_length

def find_circle_contours(image, threshold_value=80, blur_kernel_size=(5, 5), erosion_kernel_size=(7, 7), aspect_ratio_range=(0.5, 2)):
    """
    Функция для нахождения контуров, похожих на круги.

    :param image: Входное изображение.
    :param threshold_value: Пороговое значение для бинаризации.
    :param blur_kernel_size: Размер ядра для Gaussian Blur.
    :param erosion_kernel_size: Размер ядра для эрозии.
    :param aspect_ratio_range: Допустимый диапазон соотношений сторон для определения круга.
    :return: Список контуров, похожих на круги.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение размытия (Gaussian Blur)
    blurred = cv2.GaussianBlur(gray, blur_kernel_size, 0)

    # Применение эрозии для улучшения видимости контуров
    kernel = np.ones(erosion_kernel_size, np.uint8)
    eroded = cv2.erode(blurred, kernel, iterations=1)

    # Применение порогового значения для выделения черных линий
    _, binary = cv2.threshold(eroded, threshold_value, 255, cv2.THRESH_BINARY_INV)

    # Поиск контуров
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Список для хранения контуров, похожих на круги
    circle_contours = []

    # Фильтрация контуров
    for contour in contours:
        # Аппроксимация контура
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Проверка количества углов
        if True:  # Условие для фильтрации контуров с небольшим количеством углов
            # Вычисление ограничивающего прямоугольника
            x, y, w, h = cv2.boundingRect(contour)
            
            # Проверка соотношения сторон, чтобы убедиться, что это похоже на круг
            aspect_ratio = float(w) / h
            if aspect_ratio_range[0] <= aspect_ratio <= aspect_ratio_range[1]:
                circle_contours.append(contour)

    return circle_contours

# Функция для получения минимальной координаты x для каждого контура
def get_min_x(contour):
  x = cv2.boundingRect(contour)
  return x

def find_circles(image):
  leftmost_contours = find_left_counters(image.copy())
  circle_contours = find_circle_contours(image.copy())
  not_intersections = remove_intersections(circle_contours, leftmost_contours)

  top_border_counter = find_contour_by_y_order(leftmost_contours, 22)
  filtered_counters = get_counters_after_counter(not_intersections, top_border_counter, 'y')
  filtered_counters = get_counters_after_counter(filtered_counters, top_border_counter, 'x')

  bottom_border_counter = find_contour_by_y_order(leftmost_contours, 53)
  filtered_counters = get_counters_before_counter(filtered_counters, bottom_border_counter, 'y')


  # Массив для хранения пересечений по оси Y
  intersections_y = []

  for base_counter in leftmost_contours:
      # Получаем bounding box для базового контура
      x_base, y_base, w_base, h_base = cv2.boundingRect(base_counter)
      
      for filtered_counter in filtered_counters:
          # Получаем bounding box для фильтрованного контура
          x_filtered, y_filtered, w_filtered, h_filtered = cv2.boundingRect(filtered_counter)
          
          # Проверка пересечения по оси Y
          if (y_base <= y_filtered <= y_base + h_base) or (y_filtered <= y_base <= y_filtered + h_filtered):
              intersections_y.append(filtered_counter)

  filtered_counters = intersections_y
  # Сортировка контуров по площади в порядке убывания
  sorted_counters = sorted(filtered_counters, key=cv2.contourArea, reverse=True)

  # Взятие первых 97 контуров
  top_97_counters = sorted_counters[:97]



  # Сортировка контуров по минимальной координате x в порядке возрастания
  sorted_by_x = sorted(top_97_counters, key=get_min_x)

  # Взятие самых левых 90 контуров
  leftmost_90_counters = sorted_by_x[:90]

  col_counters = []
  col_counters.append([leftmost_90_counters[0]])

  for i in range(1, len(leftmost_90_counters)):
    cnt = leftmost_90_counters[i]
    prev_cnt = leftmost_90_counters[i - 1]
    x, y, w, h = cv2.boundingRect(cnt)
    prev_x, prev_y, prev_w, prev_h = cv2.boundingRect(prev_cnt)

    if  ((prev_x + prev_w - x) * 100) / w > 35:
      col_counters[len(col_counters) - 1].append(cnt)
    else:
      col_counters.append([cnt])

  left_counters = []
  for i in range(23, 53):
    left_counters.append(find_contour_by_y_order(leftmost_contours, i))

  answer_cols = []
  for col_index in range(0, len(col_counters)):
    col = col_counters[col_index]
    for cnt in col:
      x,y,w,h = cv2.boundingRect(cnt)
      for row_index in range(0, len(left_counters)):
        left_counter = left_counters[row_index]
        row_x, row_y, row_w, row_h = cv2.boundingRect(left_counter)
        if intersection_length(y, y+h, row_y, row_y + row_h) > 0:
          answer_index = (col_index + 1) % 4
          answer_cols.append([row_index + ((math.ceil((col_index + 1.0) / 4.0)) - 1) * 30, answer_index])

  answer_cols = sorted(answer_cols, key=lambda x: x[0])
  return answer_cols
