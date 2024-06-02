import cv2
import numpy as np
import display_image

def wrap_document(cv_image):
    """
    Находит и обрезает область изображения, соответствующую листу формата A4.

    :param cv_image: Изображение в формате OpenCV (numpy array)
    :return: Обрезанное изображение с листом формата A4
    """
    # Преобразование изображения в оттенки серого
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    
    # Размытие изображения для уменьшения шума
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Применение бинарного порогового преобразования
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Поиск контуров
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Сортировка контуров по площади и выбор самого большого
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    for contour in contours:
        # Аппроксимация контура
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Если контур имеет 4 вершины, предполагаем, что это лист A4
        if len(approx) == 4:
            # Получаем координаты углов
            pts = approx.reshape(4, 2)
            
            # Упорядочиваем точки по порядку: верхний левый, верхний правый, нижний правый, нижний левый
            rect = order_points(pts)
            
            # Определяем ширину и высоту нового изображения
            widthA = np.sqrt(((rect[2][0] - rect[3][0]) ** 2) + ((rect[2][1] - rect[3][1]) ** 2))
            widthB = np.sqrt(((rect[1][0] - rect[0][0]) ** 2) + ((rect[1][1] - rect[0][1]) ** 2))
            maxWidth = max(int(widthA), int(widthB))
            
            heightA = np.sqrt(((rect[1][0] - rect[2][0]) ** 2) + ((rect[1][1] - rect[2][1]) ** 2))
            heightB = np.sqrt(((rect[0][0] - rect[3][0]) ** 2) + ((rect[0][1] - rect[3][1]) ** 2))
            maxHeight = max(int(heightA), int(heightB))
            
            # Определяем точки для перспективного преобразования
            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype="float32")
            
            # Применяем перспективное преобразование
            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(cv_image, M, (maxWidth, maxHeight))
            
            return warped
    
    # Если контур не найден, возвращаем оригинальное изображение
    return cv_image

def order_points(pts):
    """
    Упорядочивает точки в порядке: верхний левый, верхний правый, нижний правый, нижний левый.

    :param pts: Массив точек (4, 2)
    :return: Упорядоченный массив точек (4, 2)
    """
    rect = np.zeros((4, 2), dtype="float32")
    
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect

for i in range(1, 16):
    # Пример использования
    # Загрузка изображения с помощью OpenCV
    cv_image = cv2.imread(f'./images/old_images/{i}.jpg')

    # Обрезка изображения с листом формата A4
    wrapped_image = wrap_document(cv_image)
    cv2.imwrite(f'./images/wrapped_old_images/{i}.jpg', wrapped_image)

