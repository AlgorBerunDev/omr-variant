import cv2
import math
from filter_contour_helper import FilterContourHelper
from intersection_helper import IntersectionHelper
from circle_analyzer import CircleAnalyzer

class FindAnswers:
  def get_min_x(self, contour):
    x = cv2.boundingRect(contour)
    return x
  
  def get_answer_circles(self, result_circles):
    return sorted(result_circles, key=self.get_min_x)[:90]
  
  def get_answers(result_image, answer_circles, result_left_contours):
    col_counters = []
    col_counters.append([answer_circles[0]])
    
    for i in range(1, len(answer_circles)):
        cnt = answer_circles[i]
        prev_cnt = answer_circles[i - 1]
        x, y, w, h = cv2.boundingRect(cnt)
        prev_x, prev_y, prev_w, prev_h = cv2.boundingRect(prev_cnt)
        
        if  ((prev_x + prev_w - x) * 100) / w > 35:
          col_counters[len(col_counters) - 1].append(cnt)
        else:
          col_counters.append([cnt])
    
    left_counters = []
    for i in range(23, 53):
        left_counters.append(FilterContourHelper.find_contour_by_y_order(result_left_contours, i))
    
    answer_cols = []
    for col_index in range(0, len(col_counters)):
        col = col_counters[col_index]
        for cnt in col:
          x,y,w,h = cv2.boundingRect(cnt)
          for row_index in range(0, len(left_counters)):
            left_counter = left_counters[row_index]
            row_x, row_y, row_w, row_h = cv2.boundingRect(left_counter)
            if IntersectionHelper.intersection_length(y, y+h, row_y, row_y + row_h) > 0:
              answer_index = (col_index + 1) % 4
              answer_cols.append([row_index + ((math.ceil((col_index + 1.0) / 4.0)) - 1) * 30, answer_index])
    
    answer_cols = sorted(answer_cols, key=lambda x: x[0])
    return answer_cols

image = cv2.imread("images/wrapped_origin/1.jpg")
circleAnalyzer = CircleAnalyzer(image)
result_circles, result_left_contours, result_image = circleAnalyzer.findContours()
circles = FindAnswers.get_answer_circles(result_circles)
print(FindAnswers.get_answers(result_image, circles, result_left_contours))
