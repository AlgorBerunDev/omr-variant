from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import cv2
import numpy as np
import base64
from image_processing.a4_detection import wrap_document
from models import circle_analyzer

app = Flask(__name__)
cors = CORS(app, resources={r"/process_frame": {"origins": "http://localhost:5173"}})

def process_image(image):
    def process():
        wrapped_image = wrap_document(image)
        result_circles, result_left_contours, result_image = circle_analyzer.findContours(wrapped_image)
        cv2.drawContours(result_image, result_circles, -1, (0, 255, 0), 2)
        return result_image

    # Устанавливаем тайм-аут в 2 секунды
    timeout = 4

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(process)
        try:
            result_image = future.result(timeout=timeout)
        except TimeoutError:
            print("Processing took too long, returning original image.")
            result_image = image

    return result_image

@app.route('/process_frame', methods=['POST'])
@cross_origin(origin='http://localhost:5173')
def process_frame():
    data = request.json
    image_data = data['image'].split(',')[1]
    image = np.frombuffer(base64.b64decode(image_data), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    processed_image = process_image(image)
    _, buffer = cv2.imencode('.jpg', processed_image)
    processed_image_data = base64.b64encode(buffer).decode('utf-8')

    return jsonify({'processed_image': f'data:image/jpeg;base64,{processed_image_data}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
