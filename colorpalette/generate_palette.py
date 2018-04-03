"""Uses k means to determine the dominate colors in an image. Displays the results in a color histogram and saves the
RGB values in a csv file. """
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import utils
import cv2
import csv
import itertools
from colorsys import rgb_to_hsv, hsv_to_rgb

DEFAULT_NUM_COLORS = 6
DEFAULT_MINV = 150
DEFAULT_MAXV = 200
SCALE = 256.0
COLORWHEEL = {"red": (255, 0, 0), "rose": (255, 0, 128), "magenta": (255, 0, 255), "violet": (128, 0, 255), "blue": (0, 0, 255), "azure": (0, 128, 255), "cyan": (0, 255, 255),
              "spring green": (0, 255, 128), "green": (0, 255, 0), "chartreuse": (128, 255, 0), "yellow": (225, 255, 0), "orange": (255, 128, 0)}


def user_input():
    palette_types = ["1) Analogous", "2) Complementary", "3) Triadic", "4) Pastel", "5) Monochromatic", "6) Bright"]
    palette_choice = input("Select one of the following palette types: " + ' '.join(palette_types) + "\n")
    return palette_types[palette_choice-1][3:]

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


def dominant_colors(image):
    # cluster the pixel intensities
    clt = KMeans(n_clusters=DEFAULT_NUM_COLORS)
    clt.fit(image)

    # build histogram of clusters and create a figure
    # representing the number of pixels labeled to each color
    hist = utils.centroid_histogram(clt)
    bar = utils.plot_colors(hist, clt.cluster_centers_)

    # extract the RGB pixel values
    row = [tuple(x) for x in bar]

    # make a list of lists containing the RGB values for all the colors in the histogram
    palette = []
    for arr in list(row[1]):
        # print([arr[0], arr[1], arr[2]])
        palette.append([arr[0], arr[1], arr[2]])

    # remove duplicates in the color list
    palette = list(palette for palette, _ in itertools.groupby(palette))
    print(palette)
    return bar, palette


def format_palette(palette):
    # convert RGB to hex and change array of RGB values to tuple
    hex = []
    rgb = []
    for clr in palette:
        hex.append("#{0:02x}{1:02x}{2:02x}".format(clr[0], clr[1], clr[2]))
        rgb.append(tuple(clr))

    return hex, rgb


def show_colors(bar):
    # show our color bar
    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    plt.savefig("result4.png")
    plt.show()
    plt.close()


def edit_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # TESTING: show our image
    # cv2.imshow('image',image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # reshape image to list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    image2 = []
    for pix in image:
        pix = clamp(pix, DEFAULT_MINV, DEFAULT_MAXV)
        image2.append(pix)
    return image2


if __name__ == '__main__':
    # ask for user input
    type = user_input()
    # print(type)

    # create csv file with results
    file = csv.writer(open('palettes2.csv', 'wb'))
    file.writerow(['image name', 'RGB', 'Hex'])

    # load image and convert from BGR to RBG
    image_path = 'test2.jpg'
    image = edit_image(image_path)

    # find dominate colors
    bar, palette = dominant_colors(image)

    # show colors
    show_colors(bar)

    # format data
    hex, rgb = format_palette(palette)

    # write rbg values into csv file
    file.writerow([
        image_path.encode('utf-8', 'ignore'),
        rgb,
        hex
    ])
