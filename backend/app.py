import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from clothing_detector import predict
from RecommendationSystem2 import generate_outfit
from colourDetector import detect_dominant_colour
from RecommendationSystem2 import main

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'imagesUploaded')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# UPLOAD_FOLDER = 'imagesUploaded'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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
        "url": f"/imagesUploaded/{img_path}"
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

@app.route('/api/generate', methods=['POST'])
def generate():
    """
    Collect all images in imagesUploaded, call AI prediction logic, and return result
    """
    # Step 1: Get all images
    uploads = [
        os.path.join(UPLOAD_FOLDER, f)
        for f in os.listdir(UPLOAD_FOLDER)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
    ]

    if not uploads:
        return jsonify({"error": "No uploaded images found"}), 400

    # Step 2: Call your backend AI script
    # This should return the path or data of the generated mannequin image
    output_file = main(uploads)  # returns something like 'modelClothes.png'

    # Step 3: Return the result URL or path
    return jsonify({
        "message": "Outfit generated successfully",
        "output_image": f"/uploads/{os.path.basename(output_file)}"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)