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

def crop_palette(image_path):
    """Crop a palette into the five sub colors and save the
    cropped colors in separate image files

    :param image_path: path of palette image_path
    :rtype: array of image paths belonging to the cropped colors
    """
    image= np.array(Image.open(image_path))
    width = image.shape[1]/5.0
    height = image.shape[0]
    x_index = 0
    single_color=[]
    # print(width)
    # print(height)

    for i in range(5):
        color= image[0:height, (int)(x_index):(int)(x_index + width)]
        x_index+= width
        img = Image.fromarray(color)
        img.save(image_path[0:-4]+"_"+str(i)+".png")
        single_color.append(image_path[0:-4]+"_"+str(i)+".png")
    single_color.append(image_path)
    print("PATHS", single_color)
    return single_color


def resize(image):
    """ Resizes image that user uploads if it is too large and replaces it

    :param image: Pillow Image that user uploaded
    """
    image= np.array(image)
    print(image.shape[1], image.shape[0])
    if image.shape[1] > 600 or image.shape[0] > 600:
        r = 600.0 / image.shape[1]
        dim = (600, int(image.shape[0] * r))
        # perform the actual resizing of the image
        image = Image.fromarray(image)
        image = image.resize(dim, resample=PIL.Image.LANCZOS)
        return image

def crop_img(image_path, bounds, count):
    """ Crops an image based on the bounds that the user selects from the
    crop tool. Saves the crop image in a new file.

    :param image_path: path of uploaded image
    :param bounds: crop BOUNDS
    :param count: the number of crops done on a single image
    :rtype: image path of cropped image
    """
    top, bottom, left, right = bounds.split(', ')
    print(int(top), int(bottom), int(left), int(right))
    print(image_path)
    image = np.array(Image.open(image_path))
    height = image.shape[0]
    new_top = abs(int(top) - height)
    new_bot = abs(int(bottom) - height)
    cropped = image[new_top:new_bot, int(left):int(right)]
    new_image_path = image_path[0:-4]+"_crop" + str(count) + ".jpg"
    img = Image.fromarray(cropped)
    img.save(new_image_path)
    return new_image_path

# if __name__ == "__main__":
    # crop_img("static/img/Violet.Evergarden.723482_13.jpg", "486, 296, 126, 273")
    # image = Image.open("/home/cassandra/Pictures/DEMO/Demo0.png")
    # crop_surrounding_whitespace(image).save('/home/cassandra/Pictures/DEMO/palettes/0.png')
    # crop_palette("/home/cassandra/Pictures/DEMO/palettes/palette0.png")
    # resize("/home/cassandra/Pictures/DEMO/colorpaletteimg.jpeg")
