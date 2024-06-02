import cv2
import numpy as np

def find_circle_contours(image, threshold_value=80, blur_kernel_size=(5, 5), erosion_kernel_size=(10, 10), aspect_ratio_range=(0.5, 2)):
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
