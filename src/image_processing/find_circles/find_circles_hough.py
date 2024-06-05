import cv2
import numpy as np

def find_circles_hough():
  image = cv2.imread("3.jpg")

  # Применение эрозии для улучшения видимости контуров
  # Преобразование изображения в оттенки серого
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Tasvirni teskari o'girish
  inverted_image = cv2.bitwise_not(gray)

  # Tasvirni yaxshilash uchun Gauss filtri orqali o'tkazish
  blurred_image = cv2.GaussianBlur(inverted_image, (9, 9), 2)

  # Hough Circle Transform yordamida aylanalarni topish
  circles = cv2.HoughCircles(blurred_image, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                            param1=50, param2=30, minRadius=16, maxRadius=30)

  # Aylanalarni tasvirda chizish
  if circles is not None:
      circles = np.round(circles[0, :]).astype("int")
      for (x, y, r) in circles:
          cv2.circle(image, (x, y), r, (0, 255, 0), 4)

  # Отображение результатов
  cv2_imshow(image)
