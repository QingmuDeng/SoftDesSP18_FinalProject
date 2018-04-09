import cv2
from PIL import Image, ImageChops

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

def resize(image_path):
    image = cv2.imread(image_path)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print(image.shape[1], image.shape[0])
    if image.shape[1] > 600 or image.shape[0] > 600:
        r = 550.0 / image.shape[1]
        dim = (550, int(image.shape[0] * r))

        # perform the actual resizing of the image and show it
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite(image_path, image)

# image = Image.open("static/img/palette.png")
# crop_surrounding_whitespace(image).save('static/img/palette3.png')
# resize('static/img/team_meal.jpg')