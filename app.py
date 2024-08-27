import io
import os
import zipfile
from datetime import datetime

from flask import Flask, jsonify, make_response, render_template, request, send_file
from PIL import Image

app = Flask(__name__)

# Rate limit configuration
RATE_LIMIT_SECONDS = 5
token_request_times = {}


def get_token():
    # Generate a unique token for each request
    # You could use a session ID or some other unique identifier
    return request.cookies.get("user_token")


def rate_limit_middleware(f):
    def decorator(*args, **kwargs):
        token = get_token()
        if token:
            current_time = datetime.now()

            if token in token_request_times:
                last_request_time = token_request_times[token]
                time_since_last_request = (
                    current_time - last_request_time
                ).total_seconds()

                if time_since_last_request < RATE_LIMIT_SECONDS:
                    return jsonify(
                        {
                            "error": "Rate limit exceeded. Please wait before making another request."
                        }
                    ), 429

            token_request_times[token] = current_time
        return f(*args, **kwargs)

    return decorator


# Set the maximum file size (20MB)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20MB


def is_image(file):
    try:
        with Image.open(file.stream) as img:
            return img.format in ["JPEG", "PNG", "WEBP"]
    except Exception:
        return False


@app.route("/", methods=["GET", "POST"])
@rate_limit_middleware
def upload_file():
    if request.method == "POST":
        files = request.files.getlist("file")
        format = request.form.get("format", "webp").lower()
        quality = int(request.form.get("quality", 80))

        if len(files) > 5:
            return render_template(
                "index.html", error="You can only upload up to 5 images at a time."
            )

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

    # Set a unique token for the user
    token = request.cookies.get("user_token")
    if not token:
        token = str(datetime.now().timestamp())
        resp = make_response(render_template("index.html"))
        resp.set_cookie("user_token", token)
        return resp

    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", debug=True)
