import PIL
from PIL import Image
import numpy as np
import random
import generate_palette as gp
#from __future__ import print_function
import webcolors
from scipy.spatial import KDTree

COLORWHEEL = {"red": (255, 0, 0), "rose": (255, 0, 128), "magenta": (255, 0, 255), "violet": (128, 0, 255),
              "blue": (0, 0, 255), "azure": (0, 128, 255), "cyan": (0, 255, 255),
              "spring green": (0, 255, 128), "green": (0, 255, 0), "chartreuse": (128, 255, 0), "yellow": (225, 255, 0),
              "orange": (255, 128, 0)}
#hue ranges for color wheel degrees
MIDRED = 0
WARMRED = 15
ORANGE = 30
WARMYELLOW = 45
MIDYELLOW = 60
COOLYELLOW = 75
YELLOWGREEN = 90
WARMGREEN = 105
MIDGREEN = 120
COOLGREEN = 135
GREENCYAN = 150
WARMCYAN = 165
MIDCYAN = 180
COOLCYAN = 195
BLUECYAN = 210
COOLBLUE = 225
MIDBLUE = 240
WARMBLUE = 255
VIOLET = 270
COOLMAGENTA = 285
MIDMAGENTA = 300
WARMMAGENTA = 315
REDMAGENTA = 330
COOLRED = 345

COLORWHEEL_RANGE = {0: "MIDRED", 15: "WARMRED", 30: "ORANGE", 45: "WARMYELLOW", 60: "MIDYELLOW", 75: "COOLYELLOW",
                    90: "YELLOWGREEN", 105: "WARMGREEN", 120: "MIDGREEN", 135: "COOLGREEN", 150: "GREENCYAN",
                    165: "WARMCYAN", 180: "MIDCYAN", 195 : "COOLCYAN", 210: "BLUECYAN", 225: "COOLBLUE", 240: "MIDBLUE",
                    255 : "WARMBLUE",270 : "VIOLET", 285 : "COOLMAGENTA", 300 : "MIDMAGENTA", 315 : "WARMMAGENTA", 330 : "REDMAGENTA",
                    345 : "COOLRED"}
HVALS = dict((v,k) for k, v in COLORWHEEL_RANGE.items())

def give_color(color):
    """
    Returns string name of the color of the input h,s,v
    :param color: a hsv tuple
    :return: string corresponding to closest color on color wheel
    """
    h,s,v = color
    if 0<=h<15:
        return COLORWHEEL_RANGE.get(0)
    elif 15<=h<30:
        return COLORWHEEL_RANGE.get(15)
    elif 30<=h<45:
        return COLORWHEEL_RANGE.get(30)
    elif 45<=h<60:
        return COLORWHEEL_RANGE.get(45)
    elif 60<=h<75:
        return COLORWHEEL_RANGE.get(60)
    elif 75<=h<90:
        return COLORWHEEL_RANGE.get(75)
    elif 90<=h<105:
        return COLORWHEEL_RANGE.get(90)
    elif 105<=h<120:
        return COLORWHEEL_RANGE.get(105)
    elif 120<=h<135:
        return COLORWHEEL_RANGE.get(120)
    elif 135<=h<150:
        return COLORWHEEL_RANGE.get(135)
    elif 150<=h<165:
        return COLORWHEEL_RANGE.get(150)
    elif 165<=h<180:
        return COLORWHEEL_RANGE.get(165)
    elif 180<=h<195:
        return COLORWHEEL_RANGE.get(180)
    elif 195<=h<210:
        return COLORWHEEL_RANGE.get(195)
    elif 210<=h<225:
        return COLORWHEEL_RANGE.get(210)
    elif 255<=h<240:
        return COLORWHEEL_RANGE.get(225)
    elif 240<=h<255:
        return COLORWHEEL_RANGE.get(240)
    elif 255<=h<270:
        return COLORWHEEL_RANGE.get(255)
    elif 270<=h<285:
        return COLORWHEEL_RANGE.get(270)
    elif 285<=h<300:
        return COLORWHEEL_RANGE.get(285)
    elif 300<=h<315:
        return COLORWHEEL_RANGE.get(300)
    elif 315<=h<330:
        return COLORWHEEL_RANGE.get(315)
    elif 330<=h<345:
        return COLORWHEEL_RANGE.get(330)
    else:
        return COLORWHEEL_RANGE.get(345)


def get_complement(color):
    """
    Gives complementary color to input color using additive color wheel
    :param colorname: str of closest color name
            color: tuple of hsv
    :return: hsv value of complement
    """
    h,s,v = color
    colorname = give_color(color)
    colorvalue = HVALS.get(colorname)
    if colorvalue < 180:
        newh = 180 + h
    else:
        newh = h - 180
    return (newh, s, v)


def analogous(color):
    """
    Returns the HSV values of all of the 4 analogous complements. NOTE THAT H VALUES ARE 0-180
    :param color: tuple with HSV values of the dominant color (where input h is 0-180)
    :return:list containing the HSV values of all 5 palette colors
    """
    # Read in the RGB value and convert it to hsv
    h,s,v = gp.get_hsv(color)
    # h = h_old*2
    ranv = random.randint(-15,15)

    accent1 = (int((h-60)), s, v+ranv)
    leftdomin = (int((h-25)), s, v+ranv)
    rightdomin = (int((h+25)), s, v+ranv)
    accent2 = (int((h+60)), s, v+ranv)

    # return colors converted to RGB
    return gp.get_rgbs([accent1, leftdomin, color, rightdomin, accent2])




def midcolor(color):
    """
    Generates middle color between 2 complementary colors
    :param color1: tuple of hsv of dominant color
    :param color2: tuple of hsv of complementary color
    :return: tuple of hsv of mid color
    """
    h1, s1, v1 = color
    #h2, s2, v2 = color2
    midh = h1 + 90
    mids = random.randint(75,115)
    midv = random.randint(100,150)
    return (midh, mids, midv)


def complement_accents(color):
    """
    Returns the HSV values for the dominant and accent colors of the complementary color palette
    :param color: tuple containing HSV value
    :return: HSV tuple of accent color
    """
    h,s,v = color
    if s<210:
        news = s + random.randint(35,40)
    else:
        news = s - random.randint(35,40)
    if v < 210:
        newv = v + random.randint(35,40)
    else:
        newv = v - random.randint(35,40)
    return (h, news, newv)


def complement(color):
    """
    Generates 5 palette colors for the complementary color palette in HSV values
    :param color: input dominant color
    :return: list of tuples of HSV values
    """
    color_hsv = tuple(gp.get_hsv(color))
    complement = get_complement(color_hsv)
    domacc = complement_accents(color_hsv)
    compacc = complement_accents(complement)
    mid = midcolor(color_hsv)
    dominant = color_hsv
    print([domacc, dominant, mid, complement, compacc])
    return gp.get_rgbs([domacc, dominant, mid, complement, compacc])


def make_websafe(color):
    # lets populate some names into spatial name database
    hexnames = webcolors.css3_hex_to_names
    names = []
    positions = []

    for hex, name in hexnames.items():
        #     print(hex, name)
        names.append(name)
        positions.append(webcolors.hex_to_rgb(hex))

    spacedb = KDTree(positions)

        # query nearest point
    querycolor = color
    dist, index = spacedb.query(querycolor)

        # return a css3 compatible color in hex
    return webcolors.name_to_hex(names[index], spec=u'css3')
