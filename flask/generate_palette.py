"""Uses k means to determine the dominate colors in an image. Displays the results in a color histogram and saves the
RGB values in a csv file. """
from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt
import utils
import csv
# import itertools
from colorsys import rgb_to_hsv, hsv_to_rgb
from operator import itemgetter
from PIL import Image
import PIL
import math
import numpy as np

DEFAULT_NUM_COLORS = 5
DEFAULT_MINV = 150
DEFAULT_MAXV = 255
SCALE = 255.0
COLORWHEEL = {"red": (255, 0, 0), "rose": (255, 0, 128), "magenta": (255, 0, 255), "violet": (128, 0, 255),
              "blue": (0, 0, 255), "azure": (0, 128, 255), "cyan": (0, 255, 255),
              "spring green": (0, 255, 128), "green": (0, 255, 0), "chartreuse": (128, 255, 0), "yellow": (225, 255, 0),
              "orange": (255, 128, 0)}


def user_input():
    palette_types = ["1) Analogous", "2) Complementary", "3) Triadic", "4) Pastel", "5) Monochromatic", "6) Bright"]
    palette_choice = input("Select one of the following palette types: " + ' '.join(palette_types) + "\n")
    return palette_types[palette_choice - 1][3:]


def down_scale(x):
    """Scales the RGB by 255 down to get to the 0-1 percentage used in colorsys from
    the normal 8 bit RGB color values"""
    return x / SCALE


def up_scale(x):
    """Scales the RGB by 255 to get to the normal 8 bit RGB color values from
    the 0-1 percentage used in colorsys"""
    return int(x * SCALE)


def clamp(color, min_v, max_v):
    """clamps a color such that its value is between min_v and max_v"""
    h, s, v = rgb_to_hsv(*map(down_scale, color))
    min_v, max_v = map(down_scale, (min_v, max_v))
    v = min(max(min_v, v), max_v)
    return tuple(map(up_scale, hsv_to_rgb(h, s, v)))


def dominant_colors(image, orig_image, n=DEFAULT_NUM_COLORS):
    """Calculates the dominant colors in an image through K-means clustering
    and returns a plottable bar graph representation of the colors and a color palette
    """
    # cluster the pixel intensities
    clt = KMeans(n_clusters=n)
    clt.fit(image)

    # build histogram of clusters and create a figure
    # representing the number of pixels labeled to each color
    hist = utils.centroid_histogram(clt)
    bar = utils.plot_colors(hist, clt.cluster_centers_)

    # make a list of lists containing the centroids RGB values
    palette = clt.cluster_centers_.astype('int').tolist()

    # make a dictionary with keys being the percentages and values being the rgbs
    output_palette = {}
    for index, color in enumerate(palette):
        output_palette[hist[index]] = color

    # Output palette is in RGB
    return bar, output_palette


def get_hsvs(clrs):
    # iterate through a list of rgb values, convert into hsv, and append to another list
    return [get_hsv(clr) for clr in clrs]


def get_hsv(clr):
    # convert a single rgb value into hsv
    h, s, v = rgb_to_hsv(*map(down_scale, clr))
    h, s, v = 360 * h, 100 * s, 100 * v
    return h, s, v


def get_rgbs(clrs):
    # iterate through a list of hsv values, convert into rgb, and append to another list
    new_clrs = []
    for clr in clrs:
        new_clrs.append(get_rgb(clr))
    return new_clrs


def get_rgb(clr):
    # convert a single hsv value into rgb
    h, s, v = clr
    h, s, v = h / 360, s / 100, v / 100
    return tuple(map(up_scale, hsv_to_rgb(h, s, v)))


def get_mag(rgb):
    # return the magnitude of a rgb pixel/vector
    r, g, b = rgb
    return math.sqrt(r ** 2 + g ** 2 + b ** 2)


def get_brightness(hsv):
    # return the magnitude of just the S and V components of a hsv pixel/vector
    h, s, v = hsv
    return math.sqrt(s ** 2 + v ** 2)


def get_hexs(clrs):
    # convert RGB to hex and change array of RGB values to tuple
    hexs = []
    for clr in clrs:
        hexs.append("#{0:02x}{1:02x}{2:02x}".format(clr[0], clr[1], clr[2]))
    return hexs


# def show_colors(bar, save=None):
#     # show our color bar
#     plt.figure()
#     plt.axis("off")
#     plt.imshow(bar)
#     if save:
#         plt.savefig(save)
#     plt.show()
#     plt.close()


def cropped(image):
    # first resize image
    r = 100.0 / image.shape[1]
    dim = (100, int(image.shape[0] * r))
    image = Image.fromarray(image)
    image = image.resize(dim, resample=PIL.Image.LANCZOS)
    # iterate through the image width and height to create all possible crops
    images = []
    image = np.array(image)
    height, width = image.shape[:2]
    delta_x = int(width / 4)
    delta_y = int(height / 4)
    index_x = 0
    index_y = 0
    for i in range(0, 4):
        for j in range(0, 4):
            temp_img = image[index_y:index_y + delta_y, index_x:index_x + delta_x]
            images.append(temp_img)
            index_y += delta_y
        index_y = 0
        index_x += delta_x

    # iterate through the cropped images to generate an array of clamped pixels
    images2 = []
    for img in images:
        # reshape image to list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))
        image2 = []
        # make sure pixels are in the right brightness ranges
        for pix in img:
            pix = clamp(pix, DEFAULT_MINV, DEFAULT_MAXV)
            image2.append(pix)
        images2.append(image2)
    return images2


def edit_image(image):
    r = 100.0 / image.shape[1]
    dim = (100, int(image.shape[0] * r))

    # perform the actual resizing of the image and show it
    image = Image.fromarray(image)
    resized = image.resize(dim, resample=PIL.Image.BILINEAR)

    # reshape image to list of pixels and clamp values
    resized = np.array(resized)
    image = resized.reshape((resized.shape[0] * resized.shape[1], 3))
    image2 = []
    for pix in image:
        pix = clamp(pix, DEFAULT_MINV, DEFAULT_MAXV)
        image2.append(pix)
    return image2


def default_palette(image, orig_image):
    """

    :param image_path: The image that you want to create color palette from
    :return: list of 5 RGB values to plot for the palette
    """

    # stores the rgb and hsv info for dominant and accent colors
    dominants_rgb = []
    dominants_hsv = []
    accents_rgb = []
    accents_hsv = []
    final_palette = []

    # find top 5 dominant colors of entire image
    bar1, palette1 = dominant_colors(image, orig_image)
    print(palette1)
    # show colors
    # show_colors(bar1)

    # get the top 1 dominant color from palette1
    first = palette1.pop(max(palette1))
    dominants_hsv.append(get_hsv(first))
    dom_h = dominants_hsv[0][0]
    print(dominants_hsv)

    # Find next dominant color from palette1 that is similar to first dominant color by taking smallest difference in hue
    # Find the two potential accent colors from palette1 by picking the two dominant colors that are most different in hue to the most dominant color
    hsvs = get_hsvs(palette1.values())
    sub_hsvs = []
    for hsv in hsvs:
        sub_hsvs.append(abs(hsv[0] - dom_h))

    # print(hsvs)
    # print(sub_hsvs)

    # sort the hue differences from least difference to most difference
    hsvs.sort(key=dict(zip(hsvs, sub_hsvs)).get)
    # print(hsvs)
    dominants_hsv.append(hsvs[0])  # first elm is most dominant color
    accents_hsv.extend(hsvs[-2:])  # last elm is most diff in hue from dominant color

    max_diff2 = abs(accents_hsv[-2][0] - dom_h)  # difference between dominant and second accent
    max_diff1 = abs(accents_hsv[-1][0] - dom_h) # difference between dominant and first accent
    min_diff = abs(dominants_hsv[-1][0] - dom_h) # difference between dominant and second dominant

    # print(max_dis, min_dis)
    # print(dominants_hsv)
    # print(accents_hsv)
    dominants_rgb.extend(get_rgbs(dominants_hsv))
    accents_rgb.extend(get_rgbs(accents_hsv))
    print(dominants_rgb)
    print(accents_rgb)

    # Examine the cropped images (consider resizing the cropped images) and look for better accents
    # look for brighter accents (go by magnitude of rgb), maybe more different from dominant colors (but watch out for outliers)
    # also look for alternatives to dominant colors by also optimizing magnitude of rgb
    cropped_images = cropped(orig_image)

    for crop in cropped_images:
        # find top 3 most dominant colors in each crop image
        bar, palette = dominant_colors(crop, 3)
        # show_colors(bar)
        temp_hsvs = get_hsvs(palette.values())
        for hsv in temp_hsvs:
            rgb = get_rgb(hsv)
            mag1 = get_mag(rgb)
            brightness1 = get_brightness(hsv)
            diff = abs(hsv[0] - dom_h)
            if diff - max_diff1 > 10 and brightness1 > get_brightness(accents_hsv[-1]):
                # found a color that is more different from dominant than current 1st accent
                max_diff2 = max_diff1
                accents_rgb[-2] = accents_rgb[-1]
                accents_hsv[-2] = accents_hsv[-1]

                max_diff1 = diff
                accents_rgb[-1] = rgb
                accents_hsv[-1] = hsv
                print("replace 1st accent", rgb)

            elif diff - max_diff2 > 10 and brightness1 > get_brightness(accents_hsv[-2]):
                max_diff2 = diff
                accents_rgb[-2] = rgb
                accents_hsv[-2] = hsv
                # found a color that is more different from dominant than current 2nd accent
                print("replace 2nd accent", rgb)

            elif abs(diff - max_diff2) < 10 and mag1 > get_mag(accents_rgb[-2]):
                # found a color that is similar in hue to 2nd accent
                max_diff2 = diff
                accents_rgb[-2] = rgb
                accents_hsv[-2] = hsv
                print("maybe found a brighter color to replace 2nd accent", rgb)

            elif abs(diff - max_diff1) < 10 and mag1 > get_mag(accents_rgb[-1]):
                # found a color that is similar in hue to 1st accent
                max_diff1 = diff
                accents_rgb[-1] = rgb
                accents_hsv[-1] = hsv
                print("maybe found a brighter color to replace 1st accent", rgb)

    #Find transition dominant color and add to list of dominants
    #transdomS, transdomV = max(dominants_hsv[-1][1], dominants_hsv[0][1]), max(dominants_hsv[-1][2], dominants_hsv[0][2])
    transdomH = (abs(dominants_hsv[-1][0] - dominants_hsv[0][0])) / 2 + min(dominants_hsv[-1][0], dominants_hsv[0][0])
    transdomS = (abs(dominants_hsv[-1][1] - dominants_hsv[0][1])) / 2 + min(dominants_hsv[-1][1], dominants_hsv[0][1])
    transdomV = (abs(dominants_hsv[-1][2] - dominants_hsv[0][2])) / 2 + min(dominants_hsv[-1][2], dominants_hsv[0][2])

    dominants_hsv.insert(1, (transdomH, transdomS, transdomV))
    dominants_rgb.insert(1, get_rgb((transdomH, transdomS, transdomV)))
    dominants_rgb.extend(accents_rgb)

    return dominants_rgb
