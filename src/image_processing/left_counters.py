import cv2

def find_left_counters(image, threshold_value=50, num_contours=65):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение порогового значения для выделения объектов
    _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)

    # Поиск контуров
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Список для хранения подходящих контуров
    filtered_contours = []

    # Проход по всем найденным контурам
    for contour in contours:
        # Вычисление ограничивающего прямоугольника для каждого контура
        x, y, w, h = cv2.boundingRect(contour)
        
        # Проверка соотношений сторон
        if 2 < w / h < 5:
            filtered_contours.append(contour)

    # Сортировка контуров по координате x (самые левые)
    filtered_contours.sort(key=lambda contour: cv2.boundingRect(contour)[0])

    # Оставляем только самые левые num_contours контуров
    leftmost_contours = filtered_contours[:num_contours]

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
