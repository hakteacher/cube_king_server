from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # CORS 허용

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 샘플 분석 함수 (나중에 실제 OpenCV 처리 로직으로 대체 가능)
def analyze_cube_image(image_path):
    # 예시 큐브 상태 문자열
    cube_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
    return cube_state

@app.route('/')
def index():
    return '✅ CubeKing Flask Server is running!'

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}_{image.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)

    # 분석 실행
    cube_state = analyze_cube_image(filepath)

    return jsonify({
        'result': '큐브 분석 완료',
        'cube_state': cube_state,
        'filename': filename
    })

# Render용: 포트 10000에서 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
