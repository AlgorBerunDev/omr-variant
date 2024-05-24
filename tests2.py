# -*- coding: utf-8 -*-

from shapely.geometry import LineString
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from cv2 import imshow as cv2_imshow
import imutils
import math
import time
start_time = time.time()
from PIL import Image


def wrap_document(img):
  # Предварительная обработка изображения  --  Tasvirni oldindan qayta ishlash
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray, (5, 5), 0)
  edges = cv2.Canny(blur, 50, 150)

  # Нахождение контуров на изображении --  Tasvirdagi konturlarni topish
  contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key=cv2.contourArea, reverse=True)


  # Определение контура, который представляет собой лист формата A4  -- A4 varaqni ifodalovchi konturni aniqlash
  for contour in contours:
      # Вычисление приближенного контура -- Taxminiy konturni hisoblash
      perimeter = cv2.arcLength(contour, True)
      approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

      # Если контур имеет 4 вершины, предполагаем, что это лист формата A4 -- Agar konturning 4 ta uchi bo'lsa, uni A4 varaq deb hisoblang
      if len(approx) == 4:
          target = approx
          break

  # Применение перспективного преобразования  --Perspektivni o'zgartirishni qo'llash
  pts = target.reshape(4, 2)
  rect = np.zeros((4, 2), dtype="float32")

  # Определение порядка точек: верхний левый, верхний правый, нижний правый, нижний левый --  Ballar tartibini aniqlang: yuqori chap, yuqori o'ng, pastki o'ng, pastki chap
  s = pts.sum(axis=1)
  rect[0] = pts[np.argmin(s)]
  rect[2] = pts[np.argmax(s)]

  diff = np.diff(pts, axis=1)
  rect[1] = pts[np.argmin(diff)]
  rect[3] = pts[np.argmax(diff)]

  # Определение ширины и высоты результирующего изображения -- Olingan tasvirning kengligi va balandligini aniqlash
  (tl, tr, br, bl) = rect
  widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
  widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
  heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
  heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

  maxWidth = max(int(widthA), int(widthB))
  maxHeight = max(int(heightA), int(heightB))

  # Выполнение перспективного преобразования  -- Istiqbolli transformatsiyani amalga oshirish
  dst = np.array([
      [0, 0],
      [maxWidth - 1, 0],
      [maxWidth - 1, maxHeight - 1],
      [0, maxHeight - 1]], dtype="float32")

  transformMatrix = cv2.getPerspectiveTransform(rect, dst)
  warped = cv2.warpPerspective(img, transformMatrix, (maxWidth, maxHeight))
  cv2.imshow("Output", warped)
  return warped


def load_and_resize_image(image_path, width):
    """Загрузка и изменение размера изображения """  # Tasvirni yuklash va o'lchamini o'zgartirish
    img = cv2.imread(image_path)
    resized_image = imutils.resize(img, width=width)
    img_wrapped = wrap_document(resized_image)
    return img_wrapped


def preprocess_image(img):
    """Предварительная обработка изображения""" # Tasvirni oldindan qayta ishlash
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray, (11, 11), 1)
    canny_frame = cv2.Canny(blurred_frame, 150, 150)
    return cv2.threshold(canny_frame, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def get_contours(thresh):
  """Получение контуров из изображения""" # Tasvirdan konturlarni olish
  cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  return cnts[0] if len(cnts) == 2 else cnts[1]


def fill_with_color(cnts, img):
  # Создаем словарь сопоставления для числа вершин и цвета  Cho'qqilar soni va ranglar uchun xaritalash lug'atini yarating
  color_mapping = {
      3: (0, 255, 0),      # Зеленый = треугольник
      4: (0, 0, 255),      # Красный = квадрат
      5: (255, 0, 0),      # Синий = пятиугольник
      6: (255, 255, 0),    # Голубой = шестиугольник
      8: (255, 128, 255),  # Розовый = восьмиугольник
  }

  for cnt in cnts:
      approx = cv2.approxPolyDP(cnt, 0.05 * cv2.arcLength(cnt, True), True)
      vertices_count = len(approx)

      # Если контур соответствует одному из ключей в словаре  Agar kontur lug'atdagi kalitlardan biriga mos kelsa
      if vertices_count in color_mapping:
          cv2.drawContours(img, [cnt], 0, color_mapping[vertices_count], -1)
      # Для большего числа вершин считаем контур кругом  Ko'proq sonli cho'qqilar uchun biz konturni aylana deb hisoblaymiz
      elif vertices_count > 12:
          cv2.drawContours(img, [cnt], 0, (0, 255, 255), -1)  # Желтый = круг

  return img


def get_biggest_area_2(cnts, can_check_limit_area = False):
    # Инициализация максимальной площади и массива для хранения наибольшего контура  Eng katta konturni saqlash uchun maksimal maydon va massivni ishga tushirish
    maxArea = 0
    biggest = []

    # Перебор всех контуров Barcha konturlarni sanab o'tish
    for i in cnts :
        # Вычисление площади контура  Kontur maydonini hisoblash
        area = cv2.contourArea(i)

        # Если площадь больше 100 или разрешена проверка ограниченной области  Agar maydon 100 dan katta bo'lsa yoki cheklangan maydonni tekshirishga ruxsat berilsa
        if area > 100 or can_check_limit_area:
            # Вычисление периметра контура  Konturning perimetrini hisoblash
            peri = cv2.arcLength(i, True)

            # Приближение формы контура  Kontur shaklini yaqinlashtirish
            edges = cv2.approxPolyDP(i, 0.05*peri, True)

            # Если площадь больше максимальной и контур имеет 4 вершины (предположительно прямоугольник)  Agar maydon maksimaldan kattaroq bo'lsa va konturda 4 ta burchak bo'lsa (ehtimol, to'rtburchaklar)
            if area > maxArea and len(edges) == 4 :
                # Обновление наибольшего контура и максимальной площади  Eng katta kontur va maksimal maydonni yangilang
                biggest = edges
                maxArea = area

    # Возвращение наибольшего контура  Eng katta konturni qaytarish
    return biggest


# Функция для выделения и обработки секций изображения  Rasmning bo'limlarini tanlash va qayta ishlash funktsiyasi
def process_sections(image, coordinates):
    sectionsMark = []
    sectionThreshs = []
    biggestCounters = []
    filledSections = []

    for cordination in coordinates:
        cv2.rectangle(image, cordination[0], cordination[1], (255, 0, 0), 0)
        top, bottom, left, right = cordination[0][1], cordination[1][1], cordination[0][0], cordination[1][0]
        sectionsMark.append(image[top:bottom, left:right].copy())

    for sectionMark in sectionsMark:
        sectionThreshs.append(cv2.threshold(sectionMark, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1])

    for sectionThresh in sectionThreshs:
        cnts = cv2.findContours(sectionThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        biggest = get_biggest_area_2(cnts)
        if len(biggest) > 0:
            biggestArea = cv2.contourArea(biggest)
            biggestCounters.append([biggest, biggestArea, sectionThresh])

    for counter in biggestCounters:
        resultMark = cv2.cvtColor(counter[2], cv2.COLOR_GRAY2BGR)
        fill_with_color([counter[0]], resultMark)
        # cv2_imshow(resultMark)
    return biggestCounters


def get_extreme_points(c, extreme):
  if extreme == 'left':
    return tuple(c[c[:, :, 0].argmin()][0])
  if extreme == 'right':
    return tuple(c[c[:, :, 0].argmax()][0])
  if extreme == 'top':
    return tuple(c[c[:, :, 1].argmin()][0])
  if extreme == 'bottom':
    return tuple(c[c[:, :, 1].argmax()][0])


def calculate_point(cordinate, counter, position):
  y = get_extreme_points(counter, position)[1]
  x = get_extreme_points(counter, position)[0]
  y += cordinate[1]
  x += cordinate[0]
  return (x, y)


def omr_area_coordinates(img):
  cordinates_of_react = [
    [(0, 210), (100, 300)], # left-1
    [(620,210), (715,300)], # right-2
    [(620,10), (715,100)], # right-1
    [(620,750), (715,840)], # right-3
    [(0,750), (100,840)], # left-2
    [(620,850), (715,1011)] # right-4
  ]

  # Вызов функции для обработки секций изображения  Rasm bo'limlarini qayta ishlash uchun funktsiyani chaqirish
  biggest_counters = process_sections(img, cordinates_of_react)

  y=get_extreme_points(biggest_counters[0][0], 'bottom')[1]
  x=get_extreme_points(biggest_counters[0][0], 'right')[0]
  y=y+cordinates_of_react[0][0][1]
  x=x+cordinates_of_react[0][0][0]
  left_top_point = (x, y) # left-1

  y=get_extreme_points(biggest_counters[1][0], 'bottom')[1]
  x=get_extreme_points(biggest_counters[1][0], 'left')[0]
  y=y+cordinates_of_react[1][0][1]
  x=x+cordinates_of_react[1][0][0]
  right_top_point = (x, y) # right-2

  y=get_extreme_points(biggest_counters[1][0], 'bottom')[1]
  x=get_extreme_points(biggest_counters[1][0], 'right')[0]
  y=y+cordinates_of_react[1][0][1]
  x=x+cordinates_of_react[1][0][0]
  right_top_point1 = (x, y) # right-2

  y=get_extreme_points(biggest_counters[3][0], 'top')[1]
  x=get_extreme_points(biggest_counters[3][0], 'left')[0]
  y=y+cordinates_of_react[3][0][1]
  x=x+cordinates_of_react[3][0][0]
  right_bottom_point = (x, y) # right-3

  y=get_extreme_points(biggest_counters[4][0], 'top')[1]
  x=get_extreme_points(biggest_counters[4][0], 'right')[0]
  y=y+cordinates_of_react[4][0][1]
  x=x+cordinates_of_react[4][0][0]
  left_bottom_point = (x, y) # left-2

  min_x=left_top_point[0]
  max_x=right_top_point[0]
  min_y=right_top_point[1]
  max_y=right_bottom_point[1]

  return min_x, max_x, min_y, max_y


def get_counter_extreme_points(cnt):
  left = get_extreme_points(cnt, 'left')
  right = get_extreme_points(cnt, 'right')
  top = get_extreme_points(cnt, 'top')
  bottom = get_extreme_points(cnt, 'bottom')
  return left, right, top, bottom


def calculate_enclosing_circle(cnt):
  # Вычисление окружности, описывающей контур  Konturni tavsiflovchi doirani hisoblash
  (x,y),radius = cv2.minEnclosingCircle(cnt)
  center = (int(x),int(y))
  radius = int(radius)
  return center, radius

def get_analyze_circles_cnts(img_org, min_x, max_x, min_y, max_y):
  img = img_org.copy()

  # Преобразование изображения в оттенки серого  Rasmni kulrang rangga aylantirish
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Применение размытия Гаусса  Gauss xiralashtirishni qo'llash
  blurred = cv2.GaussianBlur(gray, (5, 5), 0)

  # Бинаризация изображения  Tasvirni binarizatsiya
  _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)

  # Поиск контуров  Konturlarni qidiring
  contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  circle_counters = []
  for cnt in contours:
    # Вычисление моментов для определения центра масс  Massalar markazini aniqlash uchun momentlarni hisoblash
    M = cv2.moments(cnt)

    # Проверка, чтобы избежать деления на ноль  Nolga bo'linmaslik uchun tekshiring
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    left, right, top, bottom = get_counter_extreme_points(cnt)

    # Проверяем, находятся ли крайние точки внутри заданного диапазона  Ekstremal nuqtalar belgilangan diapazonda yoki yo'qligini tekshirish
    if left[0] < min_x or right[0] > max_x or top[1] < min_y or bottom[1] > max_y:
      continue

    # Вычисление соотношения сторон ограничивающего прямоугольника  Chegaraviy qutining tomonlar nisbatini hisoblash
    x,y,w,h = cv2.boundingRect(cnt)
    aspect_ratio = float(w)/h

    center, radius = calculate_enclosing_circle(cnt)

    # Вычисление площади контура и окружности  Kontur va doira maydonini hisoblash
    area_cnt = cv2.contourArea(cnt)
    area_circle = np.pi * (radius**2)
    if area_circle != 0 and area_cnt > 20:
      if 0.7 < area_cnt/area_circle < 1.9:
        circle_counters.append([left, right, top, bottom])
  return circle_counters

def analyze_circles_and_draw(img_org, counters):
  img = img_org.copy()
  center, radius = calculate_enclosing_circle(cnt)

  # for i in counters:
  #   cv2.circle(img, center, radius, (0,255,0), -1)
  return img

def draw_intersect_vertical_lines(img):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  result_omr_area_coordinates = omr_area_coordinates(gray)
  min_x = result_omr_area_coordinates[0]
  max_x = result_omr_area_coordinates[1]
  min_y = result_omr_area_coordinates[2]
  max_y = result_omr_area_coordinates[3]
  extereme_counters = get_analyze_circles_cnts(img, min_x, max_x, min_y, max_y)
  height = img.shape[0]
  temp_img = img.copy()
  for item in extereme_counters:
    left_coordinate = item[0]
    left_point_x = left_coordinate[0]
    right_coordinate = item[1]
    right_point_x = right_coordinate[0]
    start_point = (left_point_x, 0)
    end_point = (right_point_x, height)
    temp_img = cv2.rectangle(temp_img, start_point, end_point, (0,250,0), -1)
  cv2_imshow(temp_img)

def draw_intersect_horizontal_lines(img):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  min_x, max_x, min_y, max_y = omr_area_coordinates(gray)
  extereme_counters = get_analyze_circles_cnts(img, min_x, max_x, min_y, max_y)
  width = img.shape[1]
  temp_img = img.copy()
  for item in extereme_counters:
    top_coordinate = item[2]
    top_point_y = top_coordinate[1]
    bottom_coordinate = item[3]
    bottom_point_y = bottom_coordinate[1]
    start_point = (0, top_point_y)
    end_point = (width, bottom_point_y)
    temp_img = cv2.rectangle(temp_img, start_point, end_point, (0,250,0), -1)
  cv2_imshow(temp_img)

img = load_and_resize_image("omr-images/5.jpg", 720)
original = img.copy()
thresh = preprocess_image(img)
cnts = get_contours(thresh)

# Преобразование изображения из цветного в оттенки серого  Tasvirni rangdan kul rangga aylantirish
gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

# Применение порогового фильтра к изображению в оттенках серого  Kulrang tasvirga chegara filtrini qo'llash
# cv2.THRESH_BINARY_INV инвертирует результирующее бинарное изображение
# cv2.THRESH_OTSU автоматически вычисляет оптимальное значение порога
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Инициализация номера области интереса (Region of Interest, ROI)  Qiziqish mintaqasi (ROI) raqamini ishga tushirish
ROI_number = 0

# Поиск контуров на бинаризованном изображении  Binarlashtirilgan tasvirda konturlarni topish
# cv2.RETR_EXTERNAL используется для извлечения только внешних контуров
# cv2.CHAIN_APPROX_SIMPLE удаляет все избыточные точки и сжимает контур, тем самым экономя память
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# В зависимости от версии OpenCV, findContours возвращает разное количество объектов.  OpenCV versiyasiga qarab findContours boshqa sonli ob'ektlarni qaytaradi.
# Это условие обеспечивает совместимость кода с разными версиями OpenCV.   Ushbu shart kodning OpenCV ning turli versiyalari bilan mos kelishini ta'minlaydi.
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

all_center_cnts = []

start_time=time.time()
for i in range(1,15):
  img = load_and_resize_image(f"omr-images/5.jpg", 720)

  original = img.copy()
  thresh = preprocess_image(img)
  cnts = get_contours(thresh)
  # draw_intersect_vertical_lines(original)
  gray = cv2.cvtColor(original.copy(), cv2.COLOR_BGR2GRAY)
  result_omr_area_coordinates = omr_area_coordinates(gray)
  min_x = result_omr_area_coordinates[0]
  max_x = result_omr_area_coordinates[1]
  min_y = result_omr_area_coordinates[2]
  max_y = result_omr_area_coordinates[3]
  finded_circles_counters = get_analyze_circles_cnts(original, min_x, max_x, min_y, max_y)
  cv2.circle(original, (min_x, min_y), 3, (0,255,0), -1)
  cv2.circle(original, (max_x, min_y), 3, (0,255,0), -1)
  cv2.line(original, (max_x - 117, min_y), (max_x - 117, max_y), (0,255,0), 1)
  cv2.line(original, (max_x - 117*2, min_y), (max_x - 117*2, max_y), (0,255,0), 1)
  cv2.line(original, (max_x - 117*3, min_y), (max_x - 117*3, max_y), (0,255,0), 1)
  cv2.line(original, (max_x - 117*4, min_y), (max_x - 117*4, max_y), (0,255,0), 1)
  for cnt in finded_circles_counters:
    points = cnt
    cnt = np.array([list(p) for p in points], dtype=np.int32).reshape((-1, 1, 2))
    center, radius = calculate_enclosing_circle(cnt)
    cv2.circle(original, center, radius, (0,255,0), -1)
    # all_center_cnts.append(center)
  # cv2_imshow(original)
  # cv2.rectangle(original, (70, 300), (160,490), (0,250,0), 2)
  # cv2.rectangle(original, (190, 300), (285,490), (0,250,0), 2)
  # cv2.rectangle(original, (310, 300), (405,490), (0,250,0), 2)
  # cv2.rectangle(original, (435, 300), (530,774), (0,250,0), 2)
  # cv2.rectangle(original, (560, 300), (660,774), (0,250,0), 2)
  total_time = time.time() - start_time
  print("Общее время выполнения: {:.2f} секунд".format(total_time))
  start_time = time.time()
  for center in all_center_cnts:
    cv2.circle(original, center, 4, (0,255,255), -1)
    cv2.imshow('original', original)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
