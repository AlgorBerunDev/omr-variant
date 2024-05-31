import cv2


def read_omr_image(image_path):
  image = cv2.imread(image_path)
  
  # OpenCV читает изображение в формате BGR, преобразуем его в RGB для корректного отображения
  image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
