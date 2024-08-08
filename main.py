from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import io
import os

app = Flask(__name__)
# Set the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        image = Image.open(file)

        # Convert image to numpy array
        np_img = np.array(image)

        # Perform manipulation (mirror the image)
        np_img = np_img[:, ::-1, :]

        # Convert back to PIL Image
        reversed_image = Image.fromarray(np_img)

        # Save the processed image to a BytesIO object
        img_io = io.BytesIO()
        reversed_image.save(img_io, format=image.format)
        img_io.seek(0)

        return send_file(img_io, mimetype='image/jpeg')
    return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'File successfully uploaded: {filename}'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


