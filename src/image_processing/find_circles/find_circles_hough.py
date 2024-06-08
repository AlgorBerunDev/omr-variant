import cv2
import numpy as np

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

def find_circles_hough(image):
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
    filtered_circles = []
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
            if mean_color[2] < 100:
                draw_text_on_image(image, f"({int(mean_color[2])})", x+20,y)
                filtered_circles.append(create_circle_contour(x,y,r))
    return filtered_circles

