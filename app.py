
from flask import Flask, render_template, request, redirect, url_for
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
USER_SITE_URL = 'http://localhost:5001/upload'  # Assuming user site runs on port 5001
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    if file.filename == '':
        return 'No selected file'
    if file:
        # Save the image locally in the admin site
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Send the image to the user site via API
        with open(filepath, 'rb') as img_file:
            files = {'image': img_file}
            response = requests.post(USER_SITE_URL, files=files)
            if response.status_code == 200:
                return redirect(url_for('index'))
            else:
                return f"Failed to send image to user site: {response.status_code}"

@app.route('/gallery')
def gallery():
    images = os.listdir(UPLOAD_FOLDER)
    return render_template('gallery.html', images=images)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Admin site running on port 5000
