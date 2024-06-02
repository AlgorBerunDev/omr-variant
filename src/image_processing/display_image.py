import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def show_image_path(image_path):
  """
  Отображает изображение по заданному пути.

  :param image_path: Путь к изображению
  """
  img = mpimg.imread(image_path)
  imgplot = plt.imshow(img)
  plt.axis('off')  # Скрыть оси
  plt.show()

def show_image_cv2(cv_image):
    """
    Отображает изображение, переданное в формате OpenCV.

    :param cv_image: Изображение в формате OpenCV (numpy array)
    """
    # Преобразование изображения из BGR (формат OpenCV) в RGB (формат Matplotlib)
    rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    
    plt.imshow(rgb_image)
    plt.axis('off')  # Скрыть оси
    plt.show()

def show_image(image):
    """
    Отображает изображение. Может принимать путь к файлу или изображение в формате OpenCV.

    :param image: Путь к изображению или изображение в формате OpenCV (numpy array)
    """
    if isinstance(image, str):
        # Если передан путь к файлу
        img = mpimg.imread(image)
    else:
        # Если передано изображение в формате OpenCV
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    plt.imshow(img)
    plt.axis('off')  # Скрыть оси
    plt.show()
