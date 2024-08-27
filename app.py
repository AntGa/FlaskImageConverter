import io
import os
import time
import zipfile

import redis
from flask import Flask, jsonify, render_template, request, send_file
from PIL import Image

app = Flask(__name__)

# Set the maximum file size (20MB)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20MB

# Redis configuration
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

# Rate limiting configuration
RATE_LIMIT = 2  # Number of requests
TIME_FRAME = 60  # Time frame in seconds


def is_image(file):
    try:
        with Image.open(file.stream) as img:
            return img.format in ["JPEG", "PNG", "WEBP"]
    except Exception:
        return False


@app.before_request
def limit_remote_addr():
    ip = request.remote_addr
    current_time = int(time.time())
    key = f"rate_limit:{ip}"

    request_count = redis_client.get(key)
    if request_count and int(request_count) >= RATE_LIMIT:
        return jsonify(
            {
                "error": "Rate limit exceeded, Please wait 2 seconds before making another request"
            }
        ), 429

    # Increment the request count and set expiration time
    redis_client.incr(key)
    redis_client.expire(key, TIME_FRAME)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        files = request.files.getlist("file")
        format = request.form.get("format", "webp").lower()
        quality = int(request.form.get("quality", 80))

        # Check file count
        if len(files) > 5:
            return render_template(
                "index.html", error="You can only upload up to 5 images at a time."
            )

        # Check file size and type
        for file in files:
            if file.content_length > app.config["MAX_CONTENT_LENGTH"]:
                return render_template(
                    "index.html", error="Each file must be less than 20MB in size."
                )
            if not is_image(file):
                return render_template(
                    "index.html",
                    error="All files must be valid image formats (JPEG, PNG, or WEBP).",
                )

        if len(files) == 1:
            file = files[0]
            image = Image.open(file.stream)

            output_io = io.BytesIO()
            save_kwargs = {}

            if format in ["jpeg", "webp"]:
                save_kwargs["quality"] = quality

            image.save(output_io, format=format.upper(), **save_kwargs)
            output_io.seek(0)

            original_filename = file.filename
            basename, ext = os.path.splitext(original_filename)
            new_filename = f"{basename}_converted.{format}"

            return send_file(
                output_io,
                mimetype=f"image/{format}",
                download_name=new_filename,
                as_attachment=True,
            )

        elif len(files) > 1:
            zip_output = io.BytesIO()
            with zipfile.ZipFile(zip_output, "w") as zipf:
                for file in files:
                    image = Image.open(file.stream)
                    output_io = io.BytesIO()
                    save_kwargs = {}

                    if format in ["jpeg", "webp"]:
                        save_kwargs["quality"] = quality

                    image.save(output_io, format=format.upper(), **save_kwargs)
                    output_io.seek(0)

                    original_filename = file.filename
                    basename, ext = os.path.splitext(original_filename)
                    new_filename = f"{basename}_converted.{format}"

                    zipf.writestr(new_filename, output_io.read())

            zip_output.seek(0)

            return send_file(
                zip_output,
                mimetype="application/zip",
                download_name="converted_images.zip",
                as_attachment=True,
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", debug=True)
