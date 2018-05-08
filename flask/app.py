"""
app.py is used to generate the user interface aspect of our project. We integrated the HTML and color palette generation
code into this python file. In the heroku version of app.py, it saves the uploaded images and palette images to AWS.
Each time the user hits the home icon, the AWS keys gets deleted.
"""

import os
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import crop_img
import main
import boto
from PIL import Image
import requests
from io import BytesIO
from boto.s3.key import Key

app = Flask(__name__)

crop_count = 0
keys = []


@app.route("/", methods=['GET', 'POST'])
def home():
    """
    This function is automatically called when the main function runs. It renders the home page html file and deletes
    the AWS keys
    :return: rendered html of home page (known as 'index.html')
    """
    global keys
    REGION_HOST = 's3.us-east-2.amazonaws.com'
    s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'),
                             host=REGION_HOST)
    b = s3conn.get_bucket(os.environ.get('S3_BUCKET_NAME'))
    for key in keys:
        b.delete_key(key)
    keys = []
    return render_template('index.html')


@app.route("/sentiment", methods=['GET', 'POST'])
def sentiment():
    """
    sentiment() renders the sentiment.html file
    :return: rendered html of image sentiment analysis feature
    """
    return render_template('sentiment.html')


@app.route("/about", methods=['GET', 'POST'])
def about():
    """
    about() renders the about.html file
    :return: rendered html of about page
    """
    return render_template('about.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    """
    This function waits until the user uploads/crops an image, grabs the color palette and color codes,
    and loads the page with the image and palettes displayed.
    :return: rendered template of image page (known as 'image.html') with the image files and color codes passed in
    """
    global crop_count
    global keys
    # initializing variables passed into image.html
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
        # check if user uploaded an image
        if "image" in request.files:
            filename = request.files["image"].filename
            filename = filename.replace("%", "")

            # connect to s3
            REGION_HOST = 's3.us-east-2.amazonaws.com'
            s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'),
                                     host=REGION_HOST)
            # open s3 bucket, create new Key/file
            # set the mimetype, content and access control
            b = s3conn.get_bucket(os.environ.get('S3_BUCKET_NAME'))  # bucket name defined in .env
            k = b.new_key(b)  # create a new Key (like a file)
            k.key = filename  # set filename
            k.set_metadata("Content-Type", request.files["image"].mimetype)  # identify MIME type
            k.set_contents_from_string(request.files["image"].stream.read())  # file contents to be added
            k.set_acl('public-read')  # make publicly readable
            keys.append(k)

            # extract the image from aws and call resize
            response = requests.get("https://s3.us-east-2.amazonaws.com/paletteful/" + filename, stream=True)
            img = Image.open(BytesIO(response.content))
            extension = filename.split(".")[-1]
            if extension in ['jpeg', 'jpg', 'JPG', 'JPEG']:
                format = 'JPEG'
            if extension in ['png']:
                format = 'PNG'
                img = img.convert('RGB')

            # resize the uploaded image if it is too big
            resized_img = crop_img.resize(img)

            buffer = BytesIO()
            resized_img.save(buffer, format=format)
            filename2 = filename[0:-1 * (len(extension) + 1)] + "_resize" + filename[-1 * (len(extension) + 1):]

            k2 = Key(b)  # create a new Key (like a file)
            k2.key = filename2  # set filename
            k2.set_contents_from_string(buffer.getvalue())  # file contents to be added
            k2.set_acl('public-read')  # make publicly readable
            keys.append(k2)

            # generate classic palette type
            palette1, rgb1, hex1 = main.generate(img, 3)
            palettes1 = crop_img.crop_palette(palette1)

            color_names1 = []

            for ind, color in enumerate(palettes1):
                # save each palette image into AWS
                buffer2 = BytesIO()
                color.save(buffer2, format=format)
                if ind == 5:
                    name = filename[0:-1 * (len(extension) + 1)] + "_palette1" + filename[-1 * (len(extension) + 1):]
                else:
                    name = filename[0:-1 * (len(extension) + 1)] + "_palette1_" + str(ind) + filename[
                                                                                             -1 * (len(extension) + 1):]
                color_names1.append(name)
                k3 = Key(b)  # create a new Key (like a file)
                k3.key = name  # set filename
                k3.set_contents_from_string(buffer2.getvalue())  # file contents to be added
                k3.set_acl('public-read')  # make publicly readable
                keys.append(k3)

            # generate default palette type
            palette2, rgb2, hex2 = main.generate(img, 1)
            palettes2 = crop_img.crop_palette(palette2)

            color_names2 = []

            for ind, color in enumerate(palettes2):
                # save each palette image into AWS
                buffer2 = BytesIO()
                color.save(buffer2, format=format)
                if ind == 5:
                    name = filename[0:-1 * (len(extension) + 1)] + "_palette2" + filename[-1 * (len(extension) + 1):]
                else:
                    name = filename[0:-1 * (len(extension) + 1)] + "_palette2_" + str(ind) + filename[
                                                                                             -1 * (len(extension) + 1):]
                color_names2.append(name)
                k3 = Key(b)  # create a new Key (like a file)
                k3.key = name  # set filename
                k3.set_contents_from_string(buffer2.getvalue())  # file contents to be added
                k3.set_acl('public-read')  # make publicly readable
                keys.append(k3)

            # generate analogous palette type
            palette3, rgb3, hex3 = main.generate(img, 2)
            palettes3 = crop_img.crop_palette(palette3)

            color_names3 = []

            for ind, color in enumerate(palettes3):
                # save each palette image into AWS
                buffer2 = BytesIO()
                color.save(buffer2, format=format)
                if ind == 5:
                    name = filename[0:-1 * (len(extension) + 1)] + "_palette3" + filename[-1 * (len(extension) + 1):]
                else:
                    name = filename[0:-1 * (len(extension) + 1)] + "_palette3_" + str(ind) + filename[
                                                                                             -1 * (len(extension) + 1):]
                color_names3.append(name)
                k3 = Key(b)  # create a new Key (like a file)
                k3.key = name  # set filename
                k3.set_contents_from_string(buffer2.getvalue())  # file contents to be added
                k3.set_acl('public-read')  # make publicly readable
                keys.append(k3)

        # check if user cropped an image
        if "bounds" in request.form:
            REGION_HOST = 's3.us-east-2.amazonaws.com'
            s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'),
                                     host=REGION_HOST)
            b = s3conn.get_bucket(os.environ.get('S3_BUCKET_NAME'))
            crop_count += 1
            text = request.form['img']
            bounds = request.form['bounds']
            response = requests.get(text, stream=True)
            img = Image.open(BytesIO(response.content))
            extension = text.split(".")[-1]
            filename2 = text.split('/')[-1]
            if extension in ['jpeg', 'jpg']:
                format = 'JPEG'
            if extension in ['png']:
                format = 'PNG'

            # crop the image
            cropped_img = crop_img.crop_img(img, bounds, crop_count)

            # generate classic palette type
            palette1, rgb1, hex1 = main.generate(cropped_img, 3)
            palettes1 = crop_img.crop_palette(palette1)

            color_names1 = []

            for ind, color in enumerate(palettes1):
                # save each palette image into AWS
                buffer2 = BytesIO()
                color.save(buffer2, format=format)
                if ind == 5:
                    name = filename2[0:-1 * (len(extension) + 1)] + "_palette1" + filename2[-1 * (len(extension) + 1):]
                else:
                    name = filename2[0:-1 * (len(extension) + 1)] + "_palette1_" + str(ind) + filename2[
                                                                                              -1 * (len(
                                                                                                  extension) + 1):]
                color_names1.append(name)
                k3 = Key(b)  # create a new Key (like a file)
                k3.key = name  # set filename
                k3.set_contents_from_string(buffer2.getvalue())  # file contents to be added
                k3.set_acl('public-read')  # make publicly readable
                keys.append(k3)

            # generate default palette type
            palette2, rgb2, hex2 = main.generate(cropped_img, 1)
            palettes2 = crop_img.crop_palette(palette2)

            color_names2 = []

            for ind, color in enumerate(palettes2):
                # save each palette image into AWS
                buffer2 = BytesIO()
                color.save(buffer2, format=format)
                if ind == 5:
                    name = filename2[0:-1 * (len(extension) + 1)] + "_palette2" + filename2[-1 * (len(extension) + 1):]
                else:
                    name = filename2[0:-1 * (len(extension) + 1)] + "_palette2_" + str(ind) + filename2[
                                                                                              -1 * (len(
                                                                                                  extension) + 1):]
                color_names2.append(name)
                k3 = Key(b)  # create a new Key (like a file)
                k3.key = name  # set filename
                k3.set_contents_from_string(buffer2.getvalue())  # file contents to be added
                k3.set_acl('public-read')  # make publicly readable
                keys.append(k3)

            # generate analogous palette type
            palette3, rgb3, hex3 = main.generate(cropped_img, 2)
            palettes3 = crop_img.crop_palette(palette3)

            color_names3 = []

            for ind, color in enumerate(palettes3):
                # save each palette image into AWS
                buffer2 = BytesIO()
                color.save(buffer2, format=format)
                if ind == 5:
                    name = filename2[0:-1 * (len(extension) + 1)] + "_palette3" + filename2[-1 * (len(extension) + 1):]
                else:
                    name = filename2[0:-1 * (len(extension) + 1)] + "_palette3_" + str(ind) + filename2[
                                                                                              -1 * (len(
                                                                                                  extension) + 1):]
                color_names3.append(name)
                k3 = Key(b)  # create a new Key (like a file)
                k3.key = name  # set filename
                k3.set_contents_from_string(buffer2.getvalue())  # file contents to be added
                k3.set_acl('public-read')  # make publicly readable
                keys.append(k3)

    return render_template('image.html', filename1=filename2, filename2=color_names1, hex1=hex1, rgb1=rgb1,
                           filename3=color_names2, hex2=hex2, rgb2=rgb2, filename4=color_names3, hex3=hex3, rgb3=rgb3,
                           bounds=bounds)


if __name__ == "__main__":
    # the main function just runs the app
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)
