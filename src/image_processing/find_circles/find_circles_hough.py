import cv2
import numpy as np

def find_circles_hough():
  image = cv2.imread("5.jpg")

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
          if mean_color[2] < 110:
            cv2.circle(image, (x, y), r, (0,255,0), -1)
            # cv2.circle(image, (x, y), r, (int(mean_color[0]), int(mean_color[1]), int(mean_color[2])), -1)

