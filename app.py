import io
import os

from flask import Flask, render_template, request, send_file
from PIL import Image

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        format = request.form.get("format", "webp").lower()
        quality = int(request.form.get("quality", 80))

        if file:
            image = Image.open(file.stream)

            output_io = io.BytesIO()
            save_kwargs = {}

            # Set the quality if the selected format supports it
            if format in ["jpeg", "webp"]:
                save_kwargs["quality"] = quality

            # Save the image to the output stream in the selected format
            image.save(output_io, format=format.upper(), **save_kwargs)
            output_io.seek(0)

            # Extract original filename and create a new filename
            original_filename = file.filename
            basename, ext = os.path.splitext(original_filename)
            new_filename = f"{basename}_converted.{format}"

            return send_file(
                output_io,
                mimetype=f"image/{format}",
                download_name=new_filename,
                as_attachment=True,  # Ensure the file is downloaded
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
