import cv2

class Image:
  def read(self, src):
    self.__image = cv2.imread(src)
  
  def set_image(self, image):
    self.__image = image
  
  def set_width(self, new_width):
    height, width = self.__image.shape[:2]
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio)
    
    self.__image = cv2.resize(self.__image, (new_width, new_height), interpolation=cv2.INTER_AREA)
  
  def get_image(self):
    return self.__image
  
  def get_width(self):
    return self.__image.shape[1]

  def get_height(self):
    return self.__image.shape[0]
  
  def draw_text_on_image(image, text, x, y):
    """
    Tasvirga berilgan koordinatalarda matn yozadi.

    Args:
    image (numpy.ndarray): Tasvir.
    text (str): Yoziladigan matn.
    x (int): Matn yoziladigan x koordinatasi.
    y (int): Matn yoziladigan y koordinatasi.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    color = (0, 255, 0)  # Oq rang
    thickness = 2
    cv2.putText(image, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)

