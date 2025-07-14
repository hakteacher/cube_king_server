from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'

# 📦 uploads 폴더가 파일로 되어 있으면 삭제
if os.path.exists(UPLOAD_FOLDER) and not os.path.isdir(UPLOAD_FOLDER):
    os.remove(UPLOAD_FOLDER)

# 📂 uploads 폴더 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return 'CubeKing Server is running!'

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    filename = f"{uuid.uuid4().hex}{os.path.splitext(image.filename)[-1]}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)

    # 🔍 큐브 분석 결과 예시 (총 54글자: 6면 * 9스티커)
    # 순서: U (윗면), R (오른쪽), F (앞면), D (아랫면), L (왼쪽), B (뒷면)
    cube_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

    return jsonify({
        'result': '큐브 분석 완료',
        'cube_state': cube_state,
        'filename': filename
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
