import matplotlib.pyplot as plt
from PIL import Image
from image_functions import read_omr_image

def display_image_by_path(image_path):
  # Открываем изображение с помощью Pillow
  image = Image.open(image_path)
  
  # Отображаем изображение с помощью matplotlib
  plt.imshow(image)
  plt.axis('off')  # Отключаем оси
  plt.show()

def display_cv2_image(img_rgb):
  plt.imshow(img_rgb)
  plt.axis('off')  # Отключаем оси
  plt.show()
