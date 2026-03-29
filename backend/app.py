import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from clothing_detector import predict
from colourDetector import detect_dominant_colour

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST','GET'])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image    = request.files['image']
    name     = request.form.get('name', '')

    img_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(img_path)

    detected_type   = predict(img_path)
    detected_colour = detect_dominant_colour(img_path)

    return jsonify({
        "message":         "Upload successful",
        "name":            name,
        "category":        detected_type,
        "detected_colour": detected_colour,
        "path":            img_path
    })

@app.route('/api/', methods=['GET'])
def home():
    return jsonify({"message": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)