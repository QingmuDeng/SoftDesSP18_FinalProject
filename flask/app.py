"""
app.py is used to generate the user interface aspect of our project. We will be integrating everything in this python file.
Flask is the main library utilized in this python script. It basically renders our html templates without having us write
javascript.
"""
# had to pip install Flask-Uploads
# kill processes: ps -fA | grep python

import os
import sys
# module_path = os.path.abspath(os.path.join('colorpalette'))
# if module_path not in sys.path:
#     sys.path.append(module_path)

from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import flask
import crop_img
import main
import glob
# from config import MEDIA_FOLDER
# from nocache import nocache
# import json, boto3
import boto
import boto3
from PIL import Image, ImageChops
import PIL
import numpy as np
import requests
from io import BytesIO

# import webbrowser
# import threading

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img/'
configure_uploads(app, photos)

crop_count = 0


@app.route("/", methods=['GET', 'POST'])
def home():
    """
    This function is automatically called when the main function runs. It renders the home page html file
    :return: rendered html of home page (known as 'index.html')
    """
    # for infile in glob.glob('static/img/*'):
    #     os.remove(infile)
    return render_template('index.html')


@app.route('/upload/<path:filename>')
def download_file(filename):
    return flask.send_from_directory(MEDIA_FOLDER, filename, as_attachment=True)


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
    # return render_template('webpage.html')
    """
    This function waits until the user uploads an image, grabs the color palette and color codes, and loads the upload
    page with the image and palette displayed.
    :return: rendered template of image page (known as 'image.html') with the image files and color codes passed in
    """
    global crop_count
    fullname = None
    if request.method == 'POST':
        # print("posting something")
        # print("requests", request.files)

        if "image" in request.files:
            S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
            # print("posted image")
            # filename = photos.save(request.files["image"])
            filename = request.files["image"].filename
            print("FILENAME", filename)
            # fullname = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
            # fullname2 = 'img/'+filename
            # # crop_img.resize(fullname)
            # print("NAME", fullname)
            # palettename, rgb, hex = main.generate(fullname)
            # s3 = boto.connect_s3()
            # bucket = s3.create_bucket('paletteful')
            # key = bucket.new_key(filename)
            # key.set_contents_from_file(request.files["image"], headers=None, replace=True, cb=None, num_cb=10, policy=None, md5=None)
            # connect to s3
            REGION_HOST = 's3.us-east-2.amazonaws.com'
            s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'),os.environ.get('AWS_SECRET_ACCESS_KEY'), host=REGION_HOST)
            # open s3 bucket, create new Key/file
            # set the mimetype, content and access control
            # print("BUCKET", os.environ.get('S3_BUCKET_NAME'))
            # print("FILE CONTENTS", request.files["image"].read())
            b = s3conn.get_bucket(os.environ.get('S3_BUCKET_NAME')) # bucket name defined in .env
            k = b.new_key(b) # create a new Key (like a file)
            k.key = filename # set filename
            k.set_metadata("Content-Type", request.files["image"].mimetype) # identify MIME type
            k.set_contents_from_string(request.files["image"].stream.read()) # file contents to be added
            k.set_acl('public-read') # make publicly readable

            #extract the image from aws and call resize
            response = requests.get("https://s3.us-east-2.amazonaws.com/paletteful/" + filename, stream=True)
            img = Image.open(BytesIO(response.content))
            print("IMAGE", type(img))
            resized_img = crop_img.resize(img)
            print("RESIZED IMAGE", type(resized_img))
            # k = b.new_key(b)  # create a new Key (like a file)
            # k.key = filename  # set filename
            # k.set_metadata("Content-Type", request.files["image"].mimetype)  # identify MIME type
            # # HELP!!! HERE!!!
            # k.set_contents_from_string()  # file contents to be added
            # k.set_acl('public-read')  # make publicly readable
            format = 'JPEG'
            buffer = BytesIO()
            resized_img.save(buffer, format=format)

            print("HELLO!", buffer.getvalue(), type(buffer.getvalue()))

            s3 = boto3.resource('s3')

            # Uploading the image
            obj = s3.Object(
                bucket_name=b,
                key=filename,
            )
            obj.put(Body=buffer.getvalue())

        if "bounds" in request.form:
            crop_count += 1
            text = request.form['img']
            bounds = request.form['bounds']
            fullname = str(text[22:])
            fullname2 = fullname[7:]
            print("THE NAME", fullname2)
            print("BOUNDS", bounds, fullname)
            croppedname = crop_img.crop_img(fullname, bounds, crop_count)
            palettename, rgb, hex = main.generate(croppedname)

    # palettename = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], "palette3.png")
    # print(palettename)
    # colors_path = crop_img.crop_palette(palettename)
    # hex = ['#4e9559', '#18960b', '#d16903', '#f8d000', '#f8d000']
    # rgb = ['(78, 149, 89)', '(24, 150, 11)', '(209, 105, 3)', '(248, 208, 0)', '(248, 208, 0)']
    # return render_template('image.html', filename1='https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, filename), filename2=colors_path, hex=hex, rgb=rgb)
    return render_template('image.html', filename1=filename)


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
