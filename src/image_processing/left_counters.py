import cv2
import numpy as np
import intersection_functions

def find_left_counters(image, threshold_value=110, num_contours=65):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blurred = cv2.GaussianBlur(gray, (3,3), 0)

    # Применение эрозии для улучшения видимости контуров
    kernel = np.ones((1,0), np.uint8)
    eroded = cv2.erode(gray, kernel, iterations=1)

    kernel = np.ones((0,1), np.uint8)
    eroded = cv2.erode(eroded, kernel, iterations=4)

    # Применение порогового значения для выделения объектов
    _, binary = cv2.threshold(eroded, threshold_value, 255, cv2.THRESH_BINARY_INV)

    # Поиск контуров
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Список для хранения подходящих контуров
    filtered_contours = []

    # Проход по всем найденным контурам
    for contour in contours:
        # Вычисление ограничивающего прямоугольника для каждого контура
        x, y, w, h = cv2.boundingRect(contour)

        # Проверка соотношений сторон
        if 1 < w / h < 7 and w*h > 600 and w*h < 1000:
            filtered_contours.append(contour)
    
    grouped_intersection = intersection_functions.group_by_intersection_by_x(filtered_contours)
    max_grouped_intersection = max(grouped_intersection, key=len)
    image_c = image.copy()
    cv2.drawContours(image_c, max_grouped_intersection, -1, (0,255,0), 2)
    # cv2.drawContours(image_c, filtered_contours, -1, (0,255,0), 2)
    cv2.imwrite("asd.jpg", image_c)

    # Сортировка контуров по координате x (самые левые)
    max_grouped_intersection.sort(key=lambda contour: cv2.boundingRect(contour)[0])

    # Оставляем только самые левые num_contours контуров
    leftmost_contours = max_grouped_intersection[:num_contours]
    
    return leftmost_contours

def find_contour_by_y_order(contours, order=1):
    contours.sort(key=lambda contour: cv2.boundingRect(contour)[1])

    # Возвращаем контур по порядковому номеру
    if 0 < order <= len(contours):
        return contours[order - 1]
    else:
        return None

def get_image_dimensions(image):
    """
    Возвращает ширину и высоту изображения.

    :param image: Входное изображение.
    :return: Кортеж (ширина, высота).
    """
    height, width = image.shape[:2]
    return width, height

for i in [1,3,4,5,12,13,14,15,16]:
    image = cv2.imread(f"./images/wrapped_origin/{i}.jpg")
    leftmost_contours = find_left_counters(image, 90)
    pass
    for cnt in leftmost_contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    order_contour = find_contour_by_y_order(leftmost_contours, 3)
    x, y, w, h = cv2.boundingRect(order_contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imwrite(f"./images/find_left_counters/{i}.jpg", image)
