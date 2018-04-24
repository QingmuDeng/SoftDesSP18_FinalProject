"""
app.py is used to generate the user interface aspect of our project. We will be integrating everything in this python file.
Flask is the main library utilized in this python script. It basically renders our html templates without having us write
javascript.
"""
# had to pip install Flask-Uploads
# kill processes: ps -fA | grep python
import os
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
# import crop_img
# import cv2
# import webbrowser
# import threading

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)


@app.route("/", methods=['GET', 'POST'])
def home():
    """
    This function is automatically called when the main function runs. It renders the home page html file
    :return: rendered html of home page (known as 'index.html')
    """
    return render_template('index.html')


@app.route("/webpage", methods=['GET', 'POST'])
def webpage():
    return render_template('webpage.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search.html')


@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    return render_template('webpage.html')
#     """
#     This function waits until the user uploads an image, grabs the color palette and color codes, and loads the upload
#     page with the image and palette displayed.
#     :return: rendered template of image page (known as 'image.html') with the image files and color codes passed in
#     """
#     fullname = None
#     print("hello")
#     if request.method == 'POST':
#         print("posting something")
#         print("requests", request.files)
#
#         if "image" in request.files:
#             print("posted image")
#             filename = photos.save(request.files["image"])
#             fullname = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
#             # crop_img.resize(fullname)
#             print(fullname)
#
#         if "bounds" in request.form:
#             text = request.form['img']
#             bounds = request.form['bounds']
#             fullname = str(text[22:])
#             print("BOUNDS", bounds, fullname)
#             # cropped_img_path = crop_img.crop_img(fullname, bounds)
#
#     palettename = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], "palette3.png")
#     # colors_path = crop_img.crop_palette(palettename)
#     hex = ['#4e9559', '#18960b', '#d16903', '#f8d000']
#     rgb = ['(78, 149, 89)', '(24, 150, 11)', '(209, 105, 3)', '(248, 208, 0)']
#     return render_template('image.html', filename1=fullname, filename2=colors_path, hex=hex, rgb=rgb)



def allowed_file(filename):
    """
    Helper function that makes sure the user inputs an image of the correct file type.
    NOTE: this function has not been integrated yet.
    :param filename: the filename of the img the user wants to upload
    :return: the complete filename needed for upload()
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    # the main function just runs the app, the commented out code automatically opens up the port for you

    # port = 5000
    # url = "http://127.0.0.1:{0}".format(port)
    #
    # threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    #
    # app.run(port=port, debug=False)
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)
