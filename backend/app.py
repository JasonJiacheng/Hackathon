import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from clothing_detector import predict
from colourDetector import detect_dominant_colour

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/api/upload', methods=['POST', 'GET'])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files['image']
    name = request.form.get('name', '') or image.filename.rsplit('.', 1)[0]

    img_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(img_path)

    detected_type = predict(img_path)
    detected_colour = detect_dominant_colour(img_path)

    return jsonify({
        "message": "Upload successful",
        "name": name,
        "category": detected_type,
        "detected_colour": detected_colour,
        "url": f"http://localhost:5000/uploads/{image.filename}"
    })


@app.route('/api/images', methods=['GET'])
def get_images():
    """
    Return all uploaded images with their category and colour info
    Supports optional query parameters for filtering:
        - category
        - color
        - search (matches name)
    """
    category_filter = request.args.get('category', 'all').lower()
    color_filter = request.args.get('color', 'all').lower()
    search_filter = request.args.get('search', '').lower()

    images = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            continue

        img_path = os.path.join(UPLOAD_FOLDER, filename)
        detected_type = predict(img_path)
        detected_colour = detect_dominant_colour(img_path)
        name = filename.rsplit('.', 1)[0]

        # Filtering
        if category_filter != 'all' and detected_type.lower() != category_filter:
            continue
        if color_filter != 'all' and detected_colour.lower() != color_filter:
            continue
        if search_filter and search_filter not in name.lower():
            continue

        images.append({
            "name": name,
            "category": detected_type,
            "detected_colour": detected_colour,
            "url": f"http://localhost:5000/uploads/{filename}"
        })

    return jsonify(images)


@app.route('/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/api/', methods=['GET'])
def home():
    return jsonify({"message": "ok"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)