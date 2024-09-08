# web server
import datetime
import os
from flask import Flask, request, render_template, jsonify
import base64
from io import BytesIO
from PIL import Image
from ultralytics import YOLO 

app = Flask(__name__)
detector = YOLO('yolov8n_wajah.pt')

# Direktori untuk menyimpan gambar
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    image_data = data.get('image')

    if not image_data:
        return jsonify({'status': 'error', 'message': 'Data tidak lengkap'}), 400

    try:
        image_str = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_str)
        image = Image.open(BytesIO(image_bytes))
        
        results = detector.predict(image)
        bounding_boxes = []
        for result in results:
            for box in result.boxes.xyxy:
                x1, y1, x2, y2 = [int(x) for x in box]
                bounding_boxes.append({
                    'x1': int(x1),
                    'y1': int(y1),
                    'x2': int(x2),
                    'y2': int(y2)
                })

        # now = datetime.datetime.now()
        # tanggal = now.strftime('%Y-%m-%d %H-%M-%S')

        # image_filename = f"{tanggal}.png"
        # image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        # image.save(image_path)

        return jsonify({
            'status': 'success',
            'message': 'Data berhasil diterima',
            'bounding_boxes': bounding_boxes
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)