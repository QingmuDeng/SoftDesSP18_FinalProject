"""
crop_img.py contains a few image editing functions that are used in app.py
"""
from PIL import Image, ImageChops
import PIL
import numpy as np


def crop_surrounding_whitespace(image):
    """Remove surrounding empty space around an image.

    This implemenation assumes that the surrounding space has the same colour
    as the top leftmost pixel.

    :param image: PIL image
    :rtype: PIL image
    """
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    if not bbox:
        return image
    return image.crop(bbox)


def crop_palette(image):
    """Crop a palette into the five sub colors and save the
    Image objects in an array

    :param image: Image object of generated palette
    :rtype: array of Image objects belonging to the cropped colors
    """
    image2 = np.array(image)
    width = image2.shape[1] / 5.0
    height = image2.shape[0]
    x_index = 0
    single_colors = []

    for i in range(5):
        color = image2[0:height, (int)(x_index):(int)(x_index + width)]
        x_index += width
        img = Image.fromarray(color)
        single_colors.append(img)
    single_colors.append(image)
    return single_colors


def resize(input):
    """ Resizes image that user uploads if it is too large and turns new Image object

    :param input: Pillow Image that user uploaded
    """
    image = np.array(input)
    image2 = input
    # check if width is too large
    if image.shape[1] > 600:
        r = 600.0 / image.shape[1]
        dim = (600, int(image.shape[0] * r))
        # perform the actual resizing of the image
        image = Image.fromarray(image)
        image2 = image.resize(dim, resample=PIL.Image.LANCZOS)
        image = np.array(image2)
    # check if height is too large
    if image.shape[0] > 600:
        r = 600.0 / image.shape[0]
        dim = (int(image.shape[1] * r), 600)
        # perform the actual resizing of the image
        image = Image.fromarray(image)
        image2 = image.resize(dim, resample=PIL.Image.LANCZOS)
    return image2


def crop_img(input, bounds):
    """ Crops an image based on the bounds that the user selects from the
    crop tool. Returns the cropped image.

    :param input: Image object of uploaded image
    :param bounds: crop bounds
    :rtype: Image object of cropped image
    """
    top, bottom, left, right = bounds.split(', ')
    image = np.array(input)
    height = image.shape[0]
    new_top = abs(int(top) - height)
    new_bot = abs(int(bottom) - height)
    cropped = image[new_top:new_bot, int(left):int(right)]
    img = Image.fromarray(cropped)
    return img

# Main function used for testing, the parameters need to be modified accordingly
# if __name__ == "__main__":
# crop_img("static/upload_imgs/Violet.Evergarden.723482_13.jpg", "486, 296, 126, 273")
# image = Image.open("/home/cassandra/Pictures/DEMO/Demo0.png")
# crop_surrounding_whitespace(image).save('/home/cassandra/Pictures/DEMO/palettes/0.png')
# crop_palette("/home/cassandra/Pictures/DEMO/palettes/palette0.png")
# resize("/home/cassandra/Pictures/DEMO/colorpaletteimg.jpeg")
