import cv2
import numpy as np
from display_image import show_image

def preprocess_image(img):
    # Предварительная обработка изображения
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return edges

def find_document_contour(edges):
    # Нахождение контуров на изображении
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Определение контура, который представляет собой лист формата A4
    for contour in contours:
        # Вычисление приближенного контура
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        # Если контур имеет 4 вершины, предполагаем, что это лист формата A4
        if len(approx) == 4:
            return approx
    return None

def get_ordered_points(pts):
    # Определение порядка точек: верхний левый, верхний правый, нижний правый, нижний левый
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def get_max_dimensions(rect):
    # Определение ширины и высоты результирующего изображения
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    return maxWidth, maxHeight

def wrap_document(img):
    edges = preprocess_image(img)
    target = find_document_contour(edges)

    if target is None:
        raise ValueError("Документ не найден")

    pts = target.reshape(4, 2)
    rect = get_ordered_points(pts)
    maxWidth, maxHeight = get_max_dimensions(rect)

    # Выполнение перспективного преобразования
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    transformMatrix = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, transformMatrix, (maxWidth, maxHeight))

    return warped

cv_image = cv2.imread('./images/1.jpg')
wrapped_img = wrap_document(cv_image)
show_image(wrapped_img)
