from flask import (
    Blueprint,
    send_file,
    request,
    render_template,
    current_app,
    url_for,
    redirect,
)
import os
from utils import extract_metadata, sanitize_image

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("homepage.html")


@main.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method != "POST":
        return redirect(url_for("main.index"))
    file = request.files.get("image")

    if not file:
        return "No image uploaded", 400

    path = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    metadata = extract_metadata(path)

    return render_template("metadata.html", metadata=metadata, filename=file.filename)


@main.route("/sanitize", methods=["GET", "POST"])
def sanitize():
    if request.method != "POST":
        return redirect(url_for("main.index"))
    file = request.files.get("image")

    if not file:
        return "No image uploaded", 400

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    sanitized_folder = current_app.config["SANITIZED_FOLDER"]

    path = os.path.join(upload_folder, file.filename)

    file.save(path)

    print(f"Uploading Folder {upload_folder}")
    print(f"Sanitizing Folder {sanitized_folder}")

    clean_path = sanitize_image(path, sanitized_folder)

    return send_file(clean_path, as_attachment=True)
