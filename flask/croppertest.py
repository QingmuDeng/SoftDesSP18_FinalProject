import os
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import crop_img
import cv2

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()