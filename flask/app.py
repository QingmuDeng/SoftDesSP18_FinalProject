# had to pip install Flask-Uploads
# kill processes: ps -fA | grep python
import os
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    print("hello")
    if request.method == 'POST':
        print("posting something")
        print("requests", request.files)
        if 'image' in request.files:
            print("posted image")
            filename = photos.save(request.files['image'])
            fullname = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
            print(fullname)
    # file = request.files['image']
    # f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    #
    # # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    # file.save(f)
    return render_template('image.html', filename=fullname)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run()