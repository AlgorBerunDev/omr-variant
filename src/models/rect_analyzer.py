import cv2
import numpy as np
from base_contour_analyzer import BaseContourAnalyzer
from intersection_helper import IntersectionHelper
from filter_contour_helper import FilterContourHelper

class RectAnalyzer(BaseContourAnalyzer):
  def __init__(self, image):
    self.__image = image

  def findContours(self, threshold_value = 100, num_contours = 65):
    gray = cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((1,1), np.uint8)
    eroded = cv2.erode(gray, kernel, iterations=1)

    _, binary = cv2.threshold(eroded, threshold_value, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Список для хранения подходящих контуров
    filtered_contours = FilterContourHelper.filter_by_aspect_ratio(contours)
    filtered_contours = IntersectionHelper.get_gt_n_intersect_counters(filtered_contours, 60)
    filtered_contours = FilterContourHelper.filter_by_area_ratio(filtered_contours)

    # Сортировка контуров по координате x (самые левые)
    filtered_contours.sort(key=lambda contour: cv2.boundingRect(contour)[0])

    # Оставляем только самые левые num_contours контуров
    return filtered_contours[:num_contours]
