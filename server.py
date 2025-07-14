from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': '이미지 없음'}), 400

    image = request.files['image']
    filename = image.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)

    # 여기에 나중에 분석 로직 추가 가능
    return jsonify({'result': '큐브 분석 완료', 'filename': filename})

if __name__ == '__main__':
    app.run(debug=True)
