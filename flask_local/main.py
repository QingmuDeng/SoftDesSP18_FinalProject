"""
main.py is called in app.py and can generate the three types of color palettes by executing functions in generate_palette.py
"""
from generate_palette import *
import utils


def generate(input, type):
    """
    Generates classic, default, or analogous color palettes based on the type.
    :param input: Image object that palette will be generated from
    :param type: 1 stands for default, 2 for analogous, and 3 for classic
    :return: Image object of palette and lists of hex/rgb values
    """
    final_palette = []

    orig_image = np.array(input)
    # resize the image to speed up K means clustering
    image = edit_image(orig_image)

    if type == 1:
        # generate default palette
        palette = default_palette(image, orig_image)

    elif type == 2:
        # generate analogous palette
        palette = analogous_palette(image)

    else:
        palette = classic_palette(input)

    final_palette.extend(palette)
    hexs = get_hexs(final_palette)
    final_palette2 = np.array(final_palette)
    hist = [1.0 / len(final_palette2)] * len(final_palette2)
    bar = utils.plot_colors(hist, final_palette2)
    return bar, final_palette, hexs
