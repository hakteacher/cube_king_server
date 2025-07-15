from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import cv2
import numpy as np
import kociemba

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'

# uploads가 파일로 되어 있으면 삭제
if os.path.exists(UPLOAD_FOLDER) and not os.path.isdir(UPLOAD_FOLDER):
    os.remove(UPLOAD_FOLDER)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 색상 분류용
COLOR_MAP = {
    'white': 'U',
    'red': 'R',
    'green': 'F',
    'yellow': 'D',
    'orange': 'L',
    'blue': 'B'
}

def get_dominant_color(bgr):
    # 단순한 BGR -> 색 이름 매핑 기준
    b, g, r = bgr
    if r > 200 and g > 200 and b > 200:
        return 'white'
    elif r > 200 and g < 100 and b < 100:
        return 'red'
    elif g > 200 and r < 100 and b < 100:
        return 'green'
    elif r > 200 and g > 200 and b < 100:
        return 'yellow'
    elif r > 200 and g > 100 and b < 50:
        return 'orange'
    elif b > 200 and g < 100 and r < 100:
        return 'blue'
    else:
        return 'white'  # fallback

def analyze_face(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (300, 300))
    step = 100
    colors = []

    for y in range(3):
        for x in range(3):
            x_start, y_start = x * step, y * step
            patch = img[y_start + 25:y_start + 75, x_start + 25:x_start + 75]
            avg_color = np.mean(patch, axis=(0, 1))
            color_name = get_dominant_color(avg_color)
            colors.append(COLOR_MAP[color_name])

    return ''.join(colors)

def translate_solution(solution):
    moves = solution.split()
    mapping = {
        'U': '윗면',
        'D': '아랫면',
        'L': '왼쪽면',
        'R': '오른쪽면',
        'F': '앞면',
        'B': '뒷면'
    }

    result = []
    for move in moves:
        face = mapping.get(move[0], move[0])
        if len(move) == 1:
            result.append(f"{face}을 시계방향으로 한 번 돌리세요")
        elif move[1] == "'":
            result.append(f"{face}을 반시계방향으로 한 번 돌리세요")
        elif move[1] == "2":
            result.append(f"{face}을 두 번 돌리세요")

    return result

@app.route('/')
def index():
    return 'CubeKing Server is running!'

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

    try:
        # 6면 각각 분석
        facelets = [analyze_face(p) for p in images]
        cube_state = ''.join(facelets)

        # 큐브 해법 계산
        solution = kociemba.solve(cube_state)
        steps = translate_solution(solution)

        return jsonify({
            'result': '큐브 분석 완료',
            'cube_state': cube_state,
            'solution': steps
        })

    except Exception as e:
        return jsonify({'error': f'분석 실패: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
