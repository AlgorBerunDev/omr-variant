import cv2
import numpy as np
from base_contour_analyzer import BaseContourAnalyzer
from image import Image
from create_contour_helper import CreateContourHelper
from rect_analyzer import RectAnalyzer
from intersection_helper import IntersectionHelper
from filter_contour_helper import FilterContourHelper

class CircleAnalyzer(BaseContourAnalyzer):
  def __init__(self, image):
    self.__image = image
  
  def findContours(self):
    result_image, result_circles, result_left_contours = self.filter_circle_iteration()
    return result_circles, result_left_contours, result_image

  def find_circles_hough(self):
    # Применение эрозии для улучшения видимости контуров
    # Преобразование изображения в оттенки серого
    image = self.__image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Tasvirni teskari o'girish
    inverted_image = cv2.bitwise_not(gray)
    
    # Tasvirni yaxshilash uchun Gauss filtri orqali o'tkazish
    blurred_image = cv2.GaussianBlur(inverted_image, (9, 9), 2)
    
    # Hough Circle Transform yordamida aylanalarni topish
    circles = cv2.HoughCircles(blurred_image, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                            param1=50, param2=30, minRadius=16, maxRadius=30)
    filtered_circles = []
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # Aylanani maska sifatida yaratish
            mask = np.zeros_like(image)
            cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
            
            # Maskani qo'llash orqali aylanani ajratish
            masked_image = cv2.bitwise_and(image, mask)
            
            # Aylanadagi ranglarning o'rtacha qiymatini hisoblash
            mean_color = cv2.mean(image, mask=mask[:, :, 0])
            
            # Aylanani o'rtacha rang bilan to'ldirish
            if mean_color[2] < 100:
                Image.draw_text_on_image(image, f"({int(mean_color[2])})", x+20,y)
                filtered_circles.append(CreateContourHelper.create_circle_contour(x,y,r))
    return filtered_circles
  
  def find_similar_circles(self, threshold_value=80, blur_kernel_size=(5, 5), erosion_kernel_size=(7, 7),
aspect_ratio_range=(0.5, 2)):
    """
    Функция для нахождения контуров, похожих на круги.

    :param image: Входное изображение.
    :param threshold_value: Пороговое значение для бинаризации.
    :param blur_kernel_size: Размер ядра для Gaussian Blur.
    :param erosion_kernel_size: Размер ядра для эрозии.
    :param aspect_ratio_range: Допустимый диапазон соотношений сторон для определения круга.
    :return: Список контуров, похожих на круги.
    """
    gray = cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)

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

  def filter_circles(self, new_width, threshold = 120, kernel_size = (5,5), blur_size = (3,3)):
    print(new_width)
    print(threshold)
    print(kernel_size)
    print(blur_size)
    pass
    # Yangi balandlikni hisoblash
    height, width = self.__image.shape[:2]
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio)
    
    # Rasmni resize qilish
    image = cv2.resize(self.__image.copy(), (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    circles = self.find_similar_circles(image, threshold, blur_size, kernel_size)
    leftmost_rect = RectAnalyzer.findContours(image)
    
    # chap tomondagi to'rtburchaklarni aynan variantlar roparasidagisi
    left_contours = []
    for left_index in range(22,52):
        left_cnt = FilterContourHelper.find_contour_by_y_order(leftmost_rect, left_index + 1)
        left_contours.append(left_cnt)
    
    # faqat chap tomondagi to'rtburchaklar bilan y o'qi bo'yicha kesishganlarini qoldiramiz
    finded_intersect_circles = []
    for left_cnt in left_contours:
        left_x, left_y, left_w, left_h = cv2.boundingRect(left_cnt)
        for circle_cnt in circles:
            circle_x, circle_y, circle_w, circle_h = cv2.boundingRect(circle_cnt)
            if IntersectionHelper.is_intersects(left_y, left_h, circle_y, circle_h):
                finded_intersect_circles.append(circle_cnt)
    # cv2.drawContours(image, finded_intersect_circles, -1, (255,0,0), 2)
    
    # eni va bo'yi nisbati bo'yicha kvadratga o'xshashlarini qoldiramiz
    filtered_circles = []
    for circle_cnt in finded_intersect_circles:
        x,y,w,h = cv2.boundingRect(circle_cnt)
        if h != 0 and 0.4 <= float(w) / float(h) <= 2.0:
            filtered_circles.append(circle_cnt)
    
    # chap tomondagi konturlar bo'lsa ularni ham tozalab tashlaymiz
    filtered_circles = IntersectionHelper.remove_intersections(filtered_circles, left_contours)
    
    # yuzalar nisbati orqali filterlaymiz
    filtered_circles_by_area_ratio = FilterContourHelper.filter_by_area_ratio(filtered_circles,0.2,4,80)
    # cv2.drawContours(image, filtered_circles_by_area_ratio, -1, (0,255,255), 2)
    
    # kichkina nuqtalarni tozalab tashlaymiz
    filter_after_remove_small_contours = []
    for cnt in filtered_circles_by_area_ratio:
        current_cnt_area = cv2.contourArea(cnt)
        is_small = False
        for iteration_cnt in filtered_circles_by_area_ratio:
            iteration_cnt_area = cv2.contourArea(iteration_cnt)
            if  current_cnt_area != 0.0 and iteration_cnt_area / current_cnt_area > 3:
                is_small = True
                break
        if not is_small:
            filter_after_remove_small_contours.append(cnt)
    
    return image, filter_after_remove_small_contours, leftmost_rect

  def filter_circle_iteration(self):
    result = []
    result_image = []
    result_left_contours = []
    is_finded = False
    for size in [500, 900, 1200]:
        for kernel_size in range(1,10):
            for threshold in range(80, 130):
                for blur_size in [(3,3), (5,5), (9,9)]:
                    imm, finded_circles, left_contours = self.filter_circles(size, threshold, (kernel_size,kernel_size), blur_size)
                    if len(finded_circles) >= 97:
                        print(len(finded_circles))
                        result = finded_circles
                        result_image = imm
                        result_left_contours = left_contours
                        is_finded = True
                        break
                if is_finded:
                    break
            if is_finded:
                break
        if is_finded:
            break
    return result_image, result, result_left_contours
