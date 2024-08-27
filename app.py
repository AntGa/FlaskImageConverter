import io
import os
import zipfile

from flask import Flask, render_template, request, send_file
from PIL import Image

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        files = request.files.getlist("file")  # Correctly retrieve the list of files
        format = request.form.get("format", "webp").lower()
        quality = int(request.form.get("quality", 80))

        if len(files) == 1:
            # If only one file is uploaded, handle it directly
            file = files[0]
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
                as_attachment=True,
            )

        elif len(files) > 1:
            # If multiple files are uploaded, create a ZIP archive
            zip_output = io.BytesIO()
            with zipfile.ZipFile(zip_output, "w") as zipf:
                for file in files:
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

                    # Write the converted image to the ZIP file
                    zipf.writestr(new_filename, output_io.read())

            zip_output.seek(0)

            # Send the ZIP file as a downloadable attachment
            return send_file(
                zip_output,
                mimetype="application/zip",
                download_name="converted_images.zip",
                as_attachment=True,
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", debug=True)
