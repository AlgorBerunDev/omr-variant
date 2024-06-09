import cv2
import numpy as np

class CreateContourHelper:
  def create_horizontal_rectangle_counter(counter, max_width_point):
    """
    Создает горизонтальный контур (прямоугольник) на основе заданного контура.

    :param counter: Заданный контур.
    :param max_width_point: Максимальная точка по ширине.
    :return: Горизонтальный контур (прямоугольник).
    """
    if len(counter) == 0:
        return np.array([], dtype=np.float32)

    # Определяем ограничивающий прямоугольник для контура
    x, y, w, h = cv2.boundingRect(counter)

    # Создаем горизонтальный контур (прямоугольник)
    horizontal_rectangle_counter = np.array([[x, y], [max_width_point, y], [max_width_point, y + h], [x, y + h]], dtype=np.float32)

    return horizontal_rectangle_counter
  
  def create_circle_contour(x, y, r):
    """
    (x, y, r) formatidagi doira koordinatalari va radiusidan kontur yaratadi.

    Args:
    x (int): Doira markazining x koordinatasi.
    y (int): Doira markazining y koordinatasi.
    r (int): Doira radiusi.

    Returns:
    numpy.ndarray: Doira konturi.
    """
    circle_contour = []
    for angle in range(0, 360):
        theta = np.radians(angle)
        x_point = int(x + r * np.cos(theta))
        y_point = int(y + r * np.sin(theta))
        circle_contour.append([x_point, y_point])

    # Konturni numpy array formatiga o'tkazish
    circle_contour = np.array(circle_contour, dtype=np.int32).reshape((-1, 1, 2))
    return circle_contour
