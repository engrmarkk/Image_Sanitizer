import piexif
from PIL import Image
import os


def extract_metadata(filepath):
    img = Image.open(filepath)

    data = {
        "FILE": {
            "format": img.format,
            "mode": img.mode,
            "size": img.size,
        },
        "JFIF": dict(img.info) if img.info else {},
        "EXIF": {},
        "AI": {"flags": []},
    }

    # -----------------------------
    # JPEG EXIF SUPPORT
    # -----------------------------
    if img.format == "JPEG":
        try:
            exif = piexif.load(filepath)

            for section in ["0th", "Exif", "GPS"]:
                if section in exif and exif[section]:
                    data["EXIF"][section] = exif[section]

        except Exception:
            data["EXIF"] = {}

    # -----------------------------
    # PNG METADATA SUPPORT
    # -----------------------------
    elif img.format == "PNG":
        # PNG stores metadata in img.info
        png_meta = {}

        for k, v in img.info.items():
            png_meta[k] = v

        data["EXIF"]["PNG_TEXT"] = png_meta

    ai_flags = []

    # Software tag (AI tools like Photoshop, Canva, etc.)
    if "Software" in str(img.info):
        ai_flags.append("Software tag detected (possible editor export)")

    if img.format == "JPEG" and not data["EXIF"]:
        ai_flags.append("JPEG with no EXIF (likely stripped)")

    if img.format == "JPEG" and len(img.info) < 2:
        ai_flags.append("Minimal metadata JPEG (compressed/exported)")

    # PNG specific note
    if img.format == "PNG":
        if not img.info:
            ai_flags.append("Clean PNG (no embedded metadata)")
        else:
            ai_flags.append("PNG contains embedded text metadata")

    data["AI"]["flags"] = ai_flags

    return data


def sanitize_image(filepath, sanitized_folder):
    img = Image.open(filepath)

    filename = os.path.basename(filepath)
    clean_path = os.path.join(sanitized_folder, filename)

    if os.path.exists(clean_path):
        os.remove(clean_path)

    # remove metadata by rebuilding image
    data = list(img.getdata())
    clean_img = Image.new(img.mode, img.size)
    clean_img.putdata(data)

    clean_img.save(clean_path)

    return clean_path
