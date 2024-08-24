from io import BytesIO

from flask import Flask, render_template, request, send_file
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)

# Set maximum file size (e.g., 5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 Megabytes


@app.route("/", methods=["GET", "POST"])
def convert_image():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]

        # Check if the file has been selected
        if file.filename == "":
            return "No file selected", 400

        # Check if the file size is within the limit
        if file.content_length > MAX_FILE_SIZE:
            return "File size exceeds the maximum limit of 5 MB", 400

        try:
            # Attempt to open the file as an image
            input_image = Image.open(file.stream)
            input_image.verify()  # Verify that this is an actual image
            file.stream.seek(0)  # Reset stream position to the beginning

            # Convert to WebP
            img_io = BytesIO()
            input_image = Image.open(file.stream)  # Reopen image to avoid verify mode
            input_image.save(img_io, "WEBP", optimize=True, quality=10)
            img_io.seek(0)

            # Send the WebP image back to the user
            return send_file(
                img_io,
                mimetype="image/webp",
                as_attachment=True,
                download_name="converted_image.webp",
            )

        except UnidentifiedImageError:
            return "The uploaded file is not a valid image", 400
        except Exception as e:
            return str(e), 500

    return render_template("test.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5100)
