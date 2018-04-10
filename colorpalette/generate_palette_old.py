"""Uses k means to determine the dominate colors in an image. Displays the results in a color histogram and saves the
RGB values in a csv file. """
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import utils
import cv2
import csv
import itertools
from colorsys import rgb_to_hsv, hsv_to_rgb
from operator import itemgetter
import math
import numpy as np

DEFAULT_NUM_COLORS = 5
DEFAULT_MINV = 150
DEFAULT_MAXV = 255
SCALE = 256.0
COLORWHEEL = {"red": (255, 0, 0), "rose": (255, 0, 128), "magenta": (255, 0, 255), "violet": (128, 0, 255),
              "blue": (0, 0, 255), "azure": (0, 128, 255), "cyan": (0, 255, 255),
              "spring green": (0, 255, 128), "green": (0, 255, 0), "chartreuse": (128, 255, 0), "yellow": (225, 255, 0),
              "orange": (255, 128, 0)}


def user_input():
    palette_types = ["1) Analogous", "2) Complementary", "3) Triadic", "4) Pastel", "5) Monochromatic", "6) Bright"]
    palette_choice = input("Select one of the following palette types: " + ' '.join(palette_types) + "\n")
    return palette_types[palette_choice - 1][3:]


def down_scale(x):
    return x / SCALE


def up_scale(x):
    return int(x * SCALE)


def clamp(color, min_v, max_v):
    # clamps a color such that its value is between min_v and max_v
    h, s, v = rgb_to_hsv(*map(down_scale, color))
    min_v, max_v = map(down_scale, (min_v, max_v))
    v = min(max(min_v, v), max_v)
    return tuple(map(up_scale, hsv_to_rgb(h, s, v)))


def dominant_colors(image, n=DEFAULT_NUM_COLORS):
    # cluster the pixel intensities
    clt = KMeans(n_clusters=n)
    clt.fit(image)

    # build histogram of clusters and create a figure
    # representing the number of pixels labeled to each color
    hist = utils.centroid_histogram(clt)
    bar = utils.plot_colors(hist, clt.cluster_centers_)

    # print("hist", hist)
    # print(clt.cluster_centers_)
    # extract the RGB pixel values
    row = [tuple(x) for x in bar]

    # make a list of lists containing the RGB values for all the colors in the histogram
    palette = []
    for arr in list(row[1]):
        # print([arr[0], arr[1], arr[2]])
        palette.append([arr[0], arr[1], arr[2]])

    # remove duplicates in the color list
    palette = list(palette for palette, _ in itertools.groupby(palette))
    # print(palette)
    output_palette = {}
    for index, color in enumerate(palette):
        output_palette[hist[index]] = color
    return bar, output_palette


def get_hsvs(clrs):
    new_clrs = []
    for clr in clrs:
        new_clrs.append(get_hsv(clr))
    return new_clrs


def get_hsv(clr):
    h, s, v = rgb_to_hsv(*map(down_scale, clr))
    h, s, v = 360 * h, 100 * s, 100 * v
    return h, s, v


def get_rgbs(clrs):
    new_clrs = []
    for clr in clrs:
        new_clrs.append(get_rgb(clr))
    return new_clrs


def get_rgb(clr):
    h, s, v = clr
    h, s, v = h / 360, s / 100, v / 100
    return tuple(map(up_scale, hsv_to_rgb(h, s, v)))


def get_mag(rgb):
    r, g, b = rgb
    return math.sqrt(r ** 2 + g ** 2 + b ** 2)


def get_brightness(hsv):
    h, s, v = hsv
    return math.sqrt(s ** 2 + v ** 2)


def format_palette(palette):
    # convert RGB to hex and change array of RGB values to tuple
    hexs = []
    rgb = []
    hues = []
    saturations = []
    values = []
    for clr in palette:
        hexs.append("#{0:02x}{1:02x}{2:02x}".format(clr[0], clr[1], clr[2]))
        rgb.append(tuple(clr))
        h, s, v = get_hsv(clr)
        hues.append(h)
        saturations.append(s)
        values.append(v)

    return hexs, rgb, hues, saturations, values


def show_colors(bar, save=None):
    # show our color bar
    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    if save:
        plt.savefig(save)
    plt.show()
    plt.close()


def crop(image):
    r = 100.0 / image.shape[1]
    dim = (100, int(image.shape[0] * r))

    # perform the actual resizing of the image and show it
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    images = []
    height, width = image.shape[:2]
    delta_x = width / 4
    delta_y = height / 4
    index_x = 0
    index_y = 0
    for i in range(0, 4):
        for j in range(0, 4):
            temp_img = image[index_y:index_y + delta_y, index_x:index_x + delta_x]
            # cv2.imshow("cropped", temp_img)
            # cv2.waitKey(500)
            images.append(temp_img)
            index_y += delta_y
        index_y = 0
        index_x += delta_x

    images2 = []
    for img in images:
        # reshape image to list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))
        image2 = []
        for pix in img:
            pix = clamp(pix, DEFAULT_MINV, DEFAULT_MAXV)
            image2.append(pix)
        images2.append(image2)

    return images2


def edit_image(image):
    # TESTING: show our image
    # cv2.imshow('image',image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)  # convert it to hsv
    #
    # h, s, v = cv2.split(hsv)
    # print(s)
    # image = cv2.merge((h, s, v))
    # cv2.imshow("resized", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    r = 100.0 / image.shape[1]
    dim = (100, int(image.shape[0] * r))

    # perform the actual resizing of the image and show it
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    # cv2.imshow("resized", resized)
    # cv2.waitKey(0)

    # reshape image to list of pixels
    image = resized.reshape((resized.shape[0] * resized.shape[1], 3))
    image2 = []
    for pix in image:
        pix = clamp(pix, DEFAULT_MINV, DEFAULT_MAXV)
        image2.append(pix)
    return image2


if __name__ == '__main__':
    # ask for user input
    # type = user_input()
    # print(type)

    # create csv file with results
    file = csv.writer(open('palettes2.csv', 'wb'))
    file.writerow(['image name', 'RGB', 'Hex'])

    dominants_rgb = []
    dominants_hsv = []
    accents_rgb = []
    accents_hsv = []
    final_palette = []

    # load image and convert from BGR to RBG
    image_path = 'test4.jpg'
    orig_image = cv2.imread(image_path)
    orig_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    image = edit_image(orig_image)

    # find top 5 dominant colors of entire image
    bar1, palette1 = dominant_colors(image)
    print(palette1)
    # show colors
    # show_colors(bar1)

    # get the top 1 dominant color from palette1
    first = palette1.pop(max(palette1))
    # dominants_rgb.append(first)
    dominants_hsv.append(get_hsv(first))
    dom_h = dominants_hsv[0][0]
    print(dominants_hsv)

    # Find next dominant color from palette1 that is similar to first dominant color by taking smallest different in hue
    # Find the two potential accent colors from palette1 by picking the two dominant colors that are most different in hue to the most dominant color
    hsvs = get_hsvs(palette1.values())
    sub_hsvs = []
    for hsv in hsvs:
        sub_hsvs.append(abs(hsv[0] - dom_h))

    # print(hsvs)
    # print(sub_hsvs)

    # sort the hue differences from least difference to most difference
    # sub_hsvs = sorted(sub_hsvs, key=itemgetter(0))
    # print(sub_hsvs)
    hsvs.sort(key=dict(zip(hsvs, sub_hsvs)).get)
    # print(hsvs)
    dominants_hsv.append(hsvs[0])  # first elm is most dominant color
    accents_hsv.extend(hsvs[-2:])  # last elm is most diff in hue from dominant color

    max_diff2 = abs(accents_hsv[-2][0] - dom_h)  # difference between dominant and not as different accent
    max_diff1 = abs(accents_hsv[-1][0] - dom_h)
    min_diff = abs(dominants_hsv[-1][0] - dom_h)

    # print(max_dis, min_dis)
    # print(dominants_hsv)
    # print(accents_hsv)
    dominants_rgb.extend(get_rgbs(dominants_hsv))
    accents_rgb.extend(get_rgbs(accents_hsv))
    print(dominants_rgb)
    print(accents_rgb)

    # TODO: examine the cropped images (consider resizing the cropped images) and look for better accents
    # look for brighter accents (go by magnitude of rgb), maybe more different from dominant colors (but watch out for outliers)
    # also look for alternatives to dominant colors by also optimizing magnitude of rgb
    cropped_images = crop(orig_image)
    # find dominate colors
    all_hsvs = []
    for crop in cropped_images:
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

        all_hsvs.extend(temp_hsvs)

        # hexs, rgb, hues, saturations, values = format_palette(palette)
        # all_hues.extend(hues)
    # print(all_hsvs)
    # TESTING, display dominant and accent colors
    final_palette.extend(dominants_rgb)
    final_palette.extend(accents_rgb)
    final_palette = map(list, final_palette)
    final_palette = np.array(final_palette)
    hist = [1.0/len(final_palette)] * len(final_palette)
    print(hist)
    print(final_palette)
    bar = utils.plot_colors(hist, final_palette)
    # show_colors(bar, save="result13.png")
    show_colors(bar)
    # all_hues = np.asarray(all_hues)
    # clt = KMeans(n_clusters=4)
    # clt.fit(all_hues.reshape(-1, 1))
    # print(clt.cluster_centers_)

    # format data (final_palette)
    # hexs, rgb, hues, saturations, values = format_palette(palette1.values())
    # print(hues)
    # print(saturations)
    # print(values)
    # write rbg values into csv file
    # file.writerow([
    #     image_path.encode('utf-8', 'ignore'),
    #     rgb,
    #     hexs
    # ])