from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def analyze_cube_image(image_path):
    # 안전하게 더미 값 반환
    try:
        # 실제 분석 로직은 추후 구현
        return "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
    except Exception as e:
        print(f"분석 중 오류: {e}")
        return "ERROR"

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': '이미지 없음'}), 400

        image = request.files['image']
        filename = image.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)

        cube_state = analyze_cube_image(filepath)
        if cube_state == "ERROR":
            return jsonify({'error': '분석 실패'}), 500

        return jsonify({
            'result': '큐브 분석 완료',
            'cube_state': cube_state,
            'filename': filename
        })
    except Exception as e:
        print(f"서버 오류 발생: {e}")
        return jsonify({'error': '서버 오류', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
