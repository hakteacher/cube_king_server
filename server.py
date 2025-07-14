from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'

try:
    os.makedirs(UPLOAD_FOLDER)
except FileExistsError:
    pass

@app.route('/')
def index():
    return '큐브 분석 서버 실행 중!'

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': '이미지 없음'}), 400

    image = request.files['image']
    filename = image.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)

    # 여기서 AI 분석 함수로 처리 가능
    cube_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

    return jsonify({
        'result': '큐브 분석 완료',
        'cube_state': cube_state,
        'filename': filename
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
