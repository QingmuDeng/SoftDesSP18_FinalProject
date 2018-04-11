from default_palette import *
import colorwheel
import utils

palette = []
final_palette = []

if __name__ == "__main__":
    user_input = input("Select your palette type (1 = Default, 2 = Complementary, 3 = Analogous):")

    # load image and convert from BGR to RBG
    image_path = 'src_imgs/test6.jpg'
    orig_image = cv2.imread(image_path)
    orig_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    image = edit_image(orig_image)
    if int(user_input) == 2:

        # find top 5 dominant colors of entire image
        bar1, palette1 = dominant_colors(image, orig_image)

        # get the top 1 dominant color from palette1
        first = palette1.pop(max(palette1))
        hsv = get_hsv(first)
        palette = colorwheel.complement(hsv)
        print(str(palette))

    elif int(user_input) == 3:

        # find top 5 dominant colors of entire image
        bar1, palette1 = dominant_colors(image, orig_image)
        print(palette1)

        # get the top 1 dominant color from palette1
        first = palette1.pop(max(palette1))
        print(first)
        hsv = get_hsv(first)
        palette = colorwheel.analogous(hsv)

    else:
        palette = default_palette(image, orig_image)
        print(palette)

    final_palette.extend(palette)
    final_palette = map(list, final_palette)
    final_palette2 = np.array(final_palette)
    hist = [1.0 / len(final_palette2)] * len(final_palette2)
    bar = utils.plot_colors(hist, final_palette2)
    show_colors(bar)
