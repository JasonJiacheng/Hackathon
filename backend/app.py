import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from detector import run_detection
from database import init_db, get_db

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
init_db()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ── HOME ──────────────────────────────────────────────────────────────────────
@app.route("/api/home", methods=["GET"])
def home():
    db = get_db()
    total_items = db.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    db.close()
    return jsonify({"total_items": total_items})


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

    ## Save every detected garment as its own row in the DB
    db = get_db()
    for item in findings:
        db.execute("""
            INSERT INTO items (filename, original, annotated, garment, colour, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            filename,
            f"/api/uploads/{filename}",
            f"/api/uploads/{output_name}",
            item["garment"],
            item["colour"],
            item["confidence"]
        ))
    db.commit()
    db.close()

    return jsonify({
        "findings":     findings,
        "result_image": f"/api/uploads/{output_name}"
    })


# ── LIBRARY ───────────────────────────────────────────────────────────────────
@app.route("/api/library", methods=["GET"])
def get_library():
    db   = get_db()
    rows = db.execute(
        "SELECT * FROM items ORDER BY uploaded_at DESC"
    ).fetchall()
    db.close()
    return jsonify({"items": [dict(row) for row in rows]})


@app.route("/api/library/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    db  = get_db()
    row = db.execute(
        "SELECT original, annotated FROM items WHERE id = ?", (item_id,)
    ).fetchone()

    if not row:
        db.close()
        return jsonify({"error": "Item not found"}), 404

    # Delete image files from disk
    for url in [row["original"], row["annotated"]]:
        path = url.replace("/api/uploads/", app.config["UPLOAD_FOLDER"] + "/")
        if os.path.exists(path):
            os.remove(path)

    db.execute("DELETE FROM items WHERE id = ?", (item_id,))
    db.commit()
    db.close()
    return jsonify({"deleted": item_id})


# ── OUTFITS ───────────────────────────────────────────────────────────────────
@app.route("/api/outfits", methods=["GET"])
def get_outfits():
    return jsonify({"outfits": []})

@app.route("/api/outfits", methods=["POST"])
def save_outfit():
    data = request.json
    return jsonify({"saved": True, "outfit": data})


# ── GENERATE ──────────────────────────────────────────────────────────────────
@app.route("/api/generate", methods=["POST"])
def generate_outfit():
    data = request.json
    return jsonify({"suggested_outfit": []})


# ── SERVE IMAGES ──────────────────────────────────────────────────────────────
@app.route("/api/uploads/<filename>")
def serve_upload(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)