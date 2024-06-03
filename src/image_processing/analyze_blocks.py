import cv2

def analyze_blocks(cv2_image):
    gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray, (11, 11), 1)
    canny_frame = cv2.Canny(blurred_frame, 150, 150)
    return cv2.threshold(canny_frame, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
img = cv2.imread("./images/wrapped_origin/1.jpg")
cv2.imwrite("./images/analyze_blocks/1.jpg", analyze_blocks(img))
