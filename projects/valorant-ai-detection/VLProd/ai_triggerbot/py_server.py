import io
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from ultralytics import YOLO

# Используем кастомную модель для Valorant
model = YOLO('E:/VLProd/model/best.pt')

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image'}), 400
    file = request.files['image']
    img = Image.open(io.BytesIO(file.read())).convert('RGB')
    img_np = np.array(img)
    results = model(img_np)
    threshold = 0.05  # минимальный порог
    h, w, _ = img_np.shape
    cx, cy = w // 2, h // 2  # центр изображения (прицел)
    tolerance = 15  # зона допуска в пикселях
    found = False
    for box, cls, conf in zip(results[0].boxes.xyxy, results[0].boxes.cls, results[0].boxes.conf):
        if int(cls) in [0, 1] and float(conf) >= threshold:
            x1, y1, x2, y2 = map(int, box)
            if (x1 - tolerance) <= cx <= (x2 + tolerance) and (y1 - tolerance) <= cy <= (y2 + tolerance):
                found = True
                break
    return jsonify({'enemy': found})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
