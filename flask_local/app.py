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
# import flask2
import crop_img
import main
import glob
# from config import MEDIA_FOLDER
# from nocache import nocache
# import json, boto3
# import boto
# import boto3
from PIL import Image, ImageChops
import PIL
import numpy as np
import requests
# from io import BytesIO
# from boto.s3.key import Key

# import webbrowser
# import threading

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOADED_PHOTOS_DEST'] = 'static/upload_imgs/'
configure_uploads(app, photos)

crop_count = 0
keys = []


@app.route("/", methods=['GET', 'POST'])
def home():
    """
    This function is automatically called when the main function runs. It renders the home page html file
    :return: rendered html of home page (known as 'index.html')
    """
    # global keys
    # REGION_HOST = 's3.us-east-2.amazonaws.com'
    # s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'),
    #                          host=REGION_HOST)
    # b = s3conn.get_bucket(os.environ.get('S3_BUCKET_NAME'))
    # for key in keys:
    #     b.delete_key(key)
    # keys = []
    for infile in glob.glob('static/upload_imgs/*'):
        os.remove(infile)
    return render_template('index.html')


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
    # global keys
    fullname = None
    bounds = ""
    filename2 = ""
    color_names1 = []
    color_names2 = []
    color_names3 = []
    hex1 = []
    hex2 = []
    hex3 = []
    rgb1 = []
    rgb2 = []
    rgb3 = []
    if request.method == 'POST':
        print("posting something")
        print("requests", request.files)

        if "image" in request.files:
            # S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
            # print("posted image")
            filename = photos.save(request.files["image"])
            fullname = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
            # filename = request.files["image"].filename
            # filename = filename.replace(".", "")
            # filename = filename.replace("/", "")
            print("FILENAME", filename)
            # connect to s3
            # REGION_HOST = 's3.us-east-2.amazonaws.com'
            # s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'),
            #                          host=REGION_HOST)
            # # open s3 bucket, create new Key/file
            # # set the mimetype, content and access control
            # # print("BUCKET", os.environ.get('S3_BUCKET_NAME'))
            # # print("FILE CONTENTS", request.files["image"].read())
            # b = s3conn.get_bucket(os.environ.get('S3_BUCKET_NAME'))  # bucket name defined in .env
            # k = b.new_key(b)  # create a new Key (like a file)
            # k.key = filename  # set filename
            # k.set_metadata("Content-Type", request.files["image"].mimetype)  # identify MIME type
            # k.set_contents_from_string(request.files["image"].stream.read())  # file contents to be added
            # k.set_acl('public-read')  # make publicly readable
            # keys.append(k)

            # extract the image from aws and call resize
            # response = requests.get("https://s3.us-east-2.amazonaws.com/paletteful/" + filename, stream=True)
            # upload_imgs = Image.open(BytesIO(response.content))
            img = Image.open(fullname)
            # print("IMAGE", type(upload_imgs))
            extension = filename.split(".")[-1]
            print("EXTENSION", extension)
            if extension in ['jpeg', 'jpg', 'JPG', 'JPEG']:
                format = 'JPEG'
            if extension in ['png']:
                format = 'PNG'
                img = img.convert('RGB')
            resized_img = crop_img.resize(img)
            # print("RESIZED IMAGE", type(resized_img))

            # buffer = BytesIO()
            resized_img.save(fullname)
            filename2 = fullname
            # filename2 = filename[0:-1 * (len(extension) + 1)] + "_resize" + filename[-1 * (len(extension) + 1):]
            #
            # # print("HELLO!", type(buffer.getvalue()))
            # k2 = Key(b)  # create a new Key (like a file)
            # k2.key = filename2  # set filename
            #
            # print("NEW NAME", filename2)
            # # k2.set_metadata("Content-Type", request.files["image"].mimetype) # identify MIME type
            # k2.set_contents_from_string(buffer.getvalue())  # file contents to be added
            # k2.set_acl('public-read')  # make publicly readable
            # keys.append(k2)

            # generate color thief palette type
            palette1, rgb1, hex1 = main.generate(img, 3)
            palettes1 = crop_img.crop_palette(palette1)

            color_names1 = []

            for ind, color in enumerate(palettes1):
                # save each palette image into AWS
                # buffer2 = BytesIO()
                # color.save(buffer2, format=format)
                if ind == 5:
                    name = fullname[0:-1 * (len(extension) + 1)] + "_palette1" + filename[-1 * (len(extension) + 1):]
                    color.save(name)
                else:
                    name = fullname[0:-1 * (len(extension) + 1)] + "_palette1_" + str(ind) + filename[-1 * (len(extension) + 1):]
                    color.save(name)
                color_names1.append(name)
                # k3 = Key(b)  # create a new Key (like a file)
                # k3.key = name  # set filename
                # # print("COLOR NAME", name)
                # # k2.set_metadata("Content-Type", request.files["image"].mimetype) # identify MIME type
                # k3.set_contents_from_string(buffer2.getvalue())  # file contents to be added
                # k3.set_acl('public-read')  # make publicly readable
                # keys.append(k3)

            # generate default palette type
            palette2, rgb2, hex2 = main.generate(img, 1)
            palettes2 = crop_img.crop_palette(palette2)

            color_names2 = []

            for ind, color in enumerate(palettes2):
                # save each palette image into AWS
                # buffer2 = BytesIO()
                # color.save(buffer2, format=format)
                if ind == 5:
                    name = fullname[0:-1 * (len(extension) + 1)] + "_palette2" + filename[-1 * (len(extension) + 1):]
                    color.save(name)
                else:
                    name = fullname[0:-1 * (len(extension) + 1)] + "_palette2_" + str(ind) + filename[-1 * (len(extension) + 1):]
                    color.save(name)
                color_names2.append(name)
                # k3 = Key(b)  # create a new Key (like a file)
                # k3.key = name  # set filename
                # # print("COLOR NAME", name)
                # # k2.set_metadata("Content-Type", request.files["image"].mimetype) # identify MIME type
                # k3.set_contents_from_string(buffer2.getvalue())  # file contents to be added
                # k3.set_acl('public-read')  # make publicly readable
                # keys.append(k3)

            # generate analogous palette type
            palette3, rgb3, hex3 = main.generate(img, 2)
            palettes3 = crop_img.crop_palette(palette3)

            color_names3 = []

            for ind, color in enumerate(palettes3):
                # save each palette image into AWS
                # buffer2 = BytesIO()
                # color.save(buffer2, format=format)
                if ind == 5:
                    name = fullname[0:-1 * (len(extension) + 1)] + "_palette3" + filename[-1 * (len(extension) + 1):]
                    color.save(name)
                else:
                    name = fullname[0:-1 * (len(extension) + 1)] + "_palette3_" + str(ind) + filename[-1 * (len(extension) + 1):]
                    color.save(name)
                color_names3.append(name)
                # k3 = Key(b)  # create a new Key (like a file)
                # k3.key = name  # set filename
                # # print("COLOR NAME", name)
                # # k2.set_metadata("Content-Type", request.files["image"].mimetype) # identify MIME type
                # k3.set_contents_from_string(buffer2.getvalue())  # file contents to be added
                # k3.set_acl('public-read')  # make publicly readable
                # keys.append(k3)

        if "bounds" in request.form:
            # REGION_HOST = 's3.us-east-2.amazonaws.com'
            # s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'),
            #                          host=REGION_HOST)
            # # open s3 bucket, create new Key/file
            # # set the mimetype, content and access control
            # # print("BUCKET", os.environ.get('S3_BUCKET_NAME'))
            # # print("FILE CONTENTS", request.files["image"].read())
            # b = s3conn.get_bucket(os.environ.get('S3_BUCKET_NAME'))
            print("HELLO")
            crop_count += 1
            text = request.form['img']
            bounds = request.form['bounds']
            print("TEXT", text)
            print("BOUNDS", bounds)
            text = str(text[22:])
            # response = requests.get(text, stream=True)
            # upload_imgs = Image.open(BytesIO(response.content))
            img = Image.open(text)
            extension = text.split(".")[-1]
            filename2 = text
            if extension in ['jpeg', 'jpg', 'JPG', 'JPEG']:
                format = 'JPEG'
            if extension in ['png']:
                format = 'PNG'
                img = img.convert('RGB')
            # fullname = str(text[22:])
            # fullname2 = fullname[7:]
            # print("THE NAME", fullname2)
            print("BOUNDS", bounds)
            cropped_img = crop_img.crop_img(img, bounds)
            # generate color thief palette type
            palette1, rgb1, hex1 = main.generate(cropped_img, 3)
            palettes1 = crop_img.crop_palette(palette1)

            color_names1 = []

            for ind, color in enumerate(palettes1):
                # save each palette image into AWS
                # buffer2 = BytesIO()
                # color.save(buffer2, format=format)
                if ind == 5:
                    name = filename2[0:-1 * (len(extension) + 1)] + "_palette1" + "_" + str(crop_count) + filename2[-1 * (len(extension) + 1):]
                    color.save(name)
                else:
                    name = filename2[0:-1 * (len(extension) + 1)] + "_palette1_" + str(ind) + "_" + str(crop_count) + filename2[-1 * (len(extension) + 1):]
                    color.save(name)
                color_names1.append(name)
                # k3 = Key(b)  # create a new Key (like a file)
                # k3.key = name  # set filename
                # # print("COLOR NAME", name)
                # # k2.set_metadata("Content-Type", request.files["image"].mimetype) # identify MIME type
                # k3.set_contents_from_string(buffer2.getvalue())  # file contents to be added
                # k3.set_acl('public-read')  # make publicly readable
                # keys.append(k3)

            # generate default palette type
            palette2, rgb2, hex2 = main.generate(cropped_img, 1)
            palettes2 = crop_img.crop_palette(palette2)

            color_names2 = []

            for ind, color in enumerate(palettes2):
                # save each palette image into AWS
                # buffer2 = BytesIO()
                # color.save(buffer2, format=format)
                if ind == 5:
                    name = filename2[0:-1 * (len(extension) + 1)] + "_palette2" + "_" + str(crop_count) + filename2[-1 * (len(extension) + 1):]
                    color.save(name)
                else:
                    name = filename2[0:-1 * (len(extension) + 1)] + "_palette2_" + "_" + str(crop_count) + str(ind) + filename2[
                                                                                       -1 * (len(extension) + 1):]
                    color.save(name)
                color_names2.append(name)
                # k3 = Key(b)  # create a new Key (like a file)
                # k3.key = name  # set filename
                # # print("COLOR NAME", name)
                # # k2.set_metadata("Content-Type", request.files["image"].mimetype) # identify MIME type
                # k3.set_contents_from_string(buffer2.getvalue())  # file contents to be added
                # k3.set_acl('public-read')  # make publicly readable
                # keys.append(k3)

            # generate analogous palette type
            palette3, rgb3, hex3 = main.generate(cropped_img, 2)
            palettes3 = crop_img.crop_palette(palette3)

            color_names3 = []

            for ind, color in enumerate(palettes3):
                # save each palette image into AWS
                # buffer2 = BytesIO()
                # color.save(buffer2, format=format)
                if ind == 5:
                    name = filename2[0:-1 * (len(extension) + 1)] + "_palette3" + "_" + str(crop_count) + filename2[-1 * (len(extension) + 1):]
                    color.save(name)
                else:
                    name = filename2[0:-1 * (len(extension) + 1)] + "_palette3_" + "_" + str(crop_count) + str(ind) + filename2[
                                                                                       -1 * (len(extension) + 1):]
                    color.save(name)
                color_names3.append(name)
                # k3 = Key(b)  # create a new Key (like a file)
                # k3.key = name  # set filename
                # # print("COLOR NAME", name)
                # # k2.set_metadata("Content-Type", request.files["image"].mimetype) # identify MIME type
                # k3.set_contents_from_string(buffer2.getvalue())  # file contents to be added
                # k3.set_acl('public-read')  # make publicly readable
                # keys.append(k3)

    # palettename = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], "palette3.png")
    # print(palettename)
    # colors_path = crop_img.crop_palette(palettename)
    # hex = ['#4e9559', '#18960b', '#d16903', '#f8d000', '#f8d000']
    # rgb = ['(78, 149, 89)', '(24, 150, 11)', '(209, 105, 3)', '(248, 208, 0)', '(248, 208, 0)']
    # return render_template('image.html', filename1='https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, filename), filename2=colors_path, hex=hex, rgb=rgb)
    return render_template('image.html', filename1=filename2, filename2=color_names1, hex1=hex1, rgb1=rgb1, filename3=color_names2, hex2=hex2, rgb2=rgb2, filename4=color_names3, hex3=hex3, rgb3=rgb3, bounds=bounds)


def allowed_file(filename):
    """
    Helper function that makes sure the user inputs an image of the correct file type.
    NOTE: this function has not been integrated yet.
    :param filename: the filename of the upload_imgs the user wants to upload
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
