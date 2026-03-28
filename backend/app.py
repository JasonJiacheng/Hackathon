import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from detector import run_detection

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ── HOME ──────────────────────────────────────────────────────────────────────
@app.route("/api/home", methods=["GET"])
def home():
    # e.g. return a summary count of clothes + outfits for the dashboard
    return jsonify({
        "total_items":   0,
        "total_outfits": 0,
    })


# ── UPLOAD ────────────────────────────────────────────────────────────────────
@app.route("/api/detect", methods=["POST"])
def detect():
    file = request.files.get("image")
    if not file or file.filename == "":
        return jsonify({"error": "No image provided"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Use JPG, PNG or WEBP"}), 400

    filename    = secure_filename(file.filename)
    input_path  = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    output_name = f"detected_{filename}"
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], output_name)

    file.save(input_path)
    findings = run_detection(input_path, output_path)

    return jsonify({
        "findings":     findings,
        "result_image": f"/api/uploads/{output_name}"
    })


# ── LIBRARY ───────────────────────────────────────────────────────────────────
@app.route("/api/library", methods=["GET"])
def get_library():
    # Return all saved clothing items
    return jsonify({"items": []})

@app.route("/api/library/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    # Delete a clothing item by ID
    return jsonify({"deleted": item_id})


# ── OUTFITS ───────────────────────────────────────────────────────────────────
@app.route("/api/outfits", methods=["GET"])
def get_outfits():
    # Return all saved outfits
    return jsonify({"outfits": []})

@app.route("/api/outfits", methods=["POST"])
def save_outfit():
    # Save a new outfit (list of item IDs)
    data = request.json
    return jsonify({"saved": True, "outfit": data})

@app.route("/api/outfits/<int:outfit_id>", methods=["DELETE"])
def delete_outfit(outfit_id):
    return jsonify({"deleted": outfit_id})


# ── GENERATE ──────────────────────────────────────────────────────────────────
@app.route("/api/generate", methods=["POST"])
def generate_outfit():
    # Receive style preferences, return a suggested outfit from the library
    data = request.json   # e.g. { "style": "casual", "weather": "cold" }
    return jsonify({"suggested_outfit": []})


# ── SHARED: serve uploaded images ─────────────────────────────────────────────
@app.route("/api/uploads/<filename>")
def serve_upload(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
