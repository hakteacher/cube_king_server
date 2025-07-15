from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'

# uploads가 파일로 되어 있으면 삭제
if os.path.exists(UPLOAD_FOLDER) and not os.path.isdir(UPLOAD_FOLDER):
    os.remove(UPLOAD_FOLDER)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return 'CubeKing Server is running!'

def analyze_cube_images(image_paths):
    # 단순한 RGB 기반 색상 참조값 (실제 조명 환경에 따라 보정 필요)
    color_map = {
        'U': ([255, 255, 255], 'white'),   # 흰색
        'R': ([200, 0, 0], 'red'),         # 빨강
        'F': ([0, 200, 0], 'green'),       # 초록
        'D': ([255, 255, 0], 'yellow'),    # 노랑
        'L': ([255, 165, 0], 'orange'),    # 주황
        'B': ([0, 0, 200], 'blue'),        # 파랑
    }

    cube_state = ""

    for path in image_paths:
        img = cv2.imread(path)
        img = cv2.resize(img, (300, 300))
        center_colors = []

        # 3x3 정중앙 픽셀 위치를 기준으로 추출
        for y in range(3):
            for x in range(3):
                px = 50 + x * 100
                py = 50 + y * 100
                b, g, r = img[py, px]
                center_colors.append((r, g, b))

        # 각 픽셀을 가장 가까운 색상에 매칭
        for r, g, b in center_colors:
            min_diff = float('inf')
            face = 'U'
            for f, (ref_rgb, _) in color_map.items():
                diff = np.linalg.norm(np.array([r, g, b]) - np.array(ref_rgb))
                if diff < min_diff:
                    min_diff = diff
                    face = f
            cube_state += face

    return cube_state

@app.route('/upload', methods=['POST'])
def upload_images():
    images = []
    for i in range(6):
        img_key = f'image{i}'
        if img_key not in request.files:
            return jsonify({'error': f'{img_key}가 누락됨'}), 400

        image = request.files[img_key]
        filename = f"{uuid.uuid4().hex}{os.path.splitext(image.filename)[-1]}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)
        images.append(filepath)

    cube_state = analyze_cube_images(images)

    return jsonify({
        'result': '큐브 분석 완료',
        'cube_state': cube_state
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
