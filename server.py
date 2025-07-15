from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid

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

    # ✅ 실제 분석 로직이 들어갈 자리
    cube_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

    return jsonify({
        'result': '큐브 분석 완료',
        'cube_state': cube_state
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
