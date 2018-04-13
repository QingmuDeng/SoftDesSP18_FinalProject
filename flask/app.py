# had to pip install Flask-Uploads
# kill processes: ps -fA | grep python
import os
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import crop_img
import cv2
import webbrowser
import threading

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('cropimagetest.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    fullname = None
    print("hello")
    if request.method == 'POST':
        print("posting something")
        print("requests", request.files)
        if "image" in request.files:
            print("posted image")
            filename = photos.save(request.files["image"])
            fullname = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
            crop_img.resize(fullname)
            print(fullname)
    palettename = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], "palette3.png")
    colors_path = crop_img.crop_palette(palettename)
    hex = ['#4e9559', '#18960b', '#d16903', '#f8d000']
    rgb = ['(78, 149, 89)', '(24, 150, 11)', '(209, 105, 3)', '(248, 208, 0)']
    return render_template('image.html', filename1=fullname, filename2=colors_path, hex=hex,rgb=rgb)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    port = 5000
    url = "http://127.0.0.1:{0}".format(port)

    threading.Timer(1.25, lambda: webbrowser.open(url)).start()

    app.run(port=port, debug=False)