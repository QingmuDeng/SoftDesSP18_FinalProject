from generate_palette import *
import colorwheel
import utils
import webcolors
from PIL import Image

def generate(img_path, type):
    palette = []
    # websafe = []
    final_palette = []
    # user_input = input("Select your palette type (1 = Default, 2 = Complementary, 3 = Analogous):")
    # safe = input("Make palette web safe? [y/n]:")
    # safe = 'n'
    orig_image = np.array(Image.open(img_path))
    image = edit_image(orig_image)

    if type == 1:
        # generate default palette
        palette = default_palette(image, orig_image)

    elif type == 2:
        # generate analogous palette
        palette = analogous_palette(image, orig_image)

    # if int(user_input) == 2:
    #     # find top 5 dominant colors of entire image
    #     bar1, palette1 = dominant_colors(image, orig_image)
    #
    #     # get the top 1 dominant color from palette1
    #     first = palette1.pop(max(palette1))
    #     palette = list(colorwheel.complement(first))
    #     print("PALETTE", palette)
    #
    #
    # elif int(user_input) == 3:
    #     # find top 5 dominant colors of entire image
    #     bar1, palette1 = dominant_colors(image, orig_image)
    #
    #     # get the top 1 dominant color from palette1
    #     first = palette1.pop(max(palette1))
    #     palette = list(colorwheel.analogous(first))
    #
    #
    # elif user_input == 1:
    #     palette = default_palette(image, orig_image)
    #     print("PALETTE", palette)
    #
    # #converts colors to websafe
    # if safe=="y":
    #     for color in palette:
    #         websafe.append(colorwheel.make_websafe(color))
    #     print(websafe)
    #     for hexa in websafe:
    #         final_palette.append(webcolors.hex_to_rgb(hexa))
    # else:
    #     final_palette.extend(palette)
    # final_palette = map(list, final_palette)
    final_palette.extend(palette)
    hexs = get_hexs(final_palette)
    final_palette2 = np.array(final_palette)
    hist = [1.0 / len(final_palette2)] * len(final_palette2)
    bar = utils.plot_colors(hist, final_palette2)
    # show_colors(bar)
    # bar = Image.fromarray(bar)
    # print("BAR TYPE", type(bar))

    # new_path = img_path[0:-4]+'_p.png'
    # bar.save(new_path)
    return bar, final_palette, hexs

if __name__ == "__main__":
    main()
