import cv2
import numpy as np
import random

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
HVALS = dict((v,k) for k, v in COLORWHEEL_RANGE.iteritems())

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
        newh = ((180 + colorvalue) + (h-colorvalue))/2
    else:
        newh = ((colorvalue - 180) + (h - colorvalue))/2    #added /2 to make range 0-180
    return (newh,s,v)

def complement_accents(color):
    """
    Returns the HSV values for the dominant and accent colors of the complementary color palette
    :param color: tuple containing HSV value
    :return: HSV tuple of accent color
    """
    h,s,v = color
    if s<210:
        news = s + random.randint(35,45)
    else:
        news = s - random.randint(35,45)
    if v < 210:
        newv = 255
    else:
        newv = v - random.randint(35,45)
    return (h,news,newv)

def analogous(color):
    """
    Returns the HSV values of all of the 4 analogous complements. NOTE THAT H VALUES ARE 0-180
    :param color: tuple with HSV values of the dominant color (where input h is 0-180)
    :return:list containing the HSV values of all 5 palette colors
    """
    h_old,s,v = color
    h = h_old*2
    ranv = random.randint(-15,15)

    accent1 = (int((h-60)/2), s, v+ranv)
    leftdomin = (int((h-30)/2), s, v+ranv)
    rightdomin = (int((h+30)/2), s, v+ranv)
    accent2 = (int((h+60)/2), s, v+ranv)
    return [accent1, leftdomin, color, rightdomin, accent2]

def midcolor(color):
    """
    Generates middle color between 2 complementary colors
    :param color1: tuple of hsv of dominant color
    :param color2: tuple of hsv of complementary color
    :return: tuple of hsv of mid color
    """
    h1, s1, v1 = color
    #h2, s2, v2 = color2
    midh = int((h1 + 90)/2)
    mids = random.randint(75,115)
    midv = random.randint(100,150)
    return (midh, mids, midv)

def hsvrgbcv(color):
    """
    Takes HSV values and converts to RGB tuple for OpenCV
    :param color:
    :return:
    """
    rgb = cv2.cvtColor(np.uint8([[list(color)]]), cv2.COLOR_HSV2RGB)
    rgbcolor = rgb[0][0][0], rgb[0][0][1], rgb[0][0][2]
    return rgbcolor

def complement(color):
    """
    Generates 5 palette colors for the complementary color palette in HSV values
    :param color: input dominant color
    :return: list of tuples of HSV values
    """
    complement = hsvrgbcv(get_complement(color))
    domacc = hsvrgbcv(complement_accents(color))
    compacc = hsvrgbcv(complement_accents(complement))
    mid = hsvrgbcv(midcolor(color))
    dominant = hsvrgbcv(color)
    return [domacc, dominant, mid, complement, compacc]

def visualize(hsv, colorstr):
    canvas = np.zeros((100, 100, 3), np.uint8)
    canvas[:, :] = hsv
    canvas = cv2.cvtColor(canvas, cv2.COLOR_HSV2BGR)
    cv2.imshow(colorstr, canvas)

#TODO: generate 3 midcolors to go gradient between the two colors or generate two accent colors and one midtone color
# ogH = random.randint(0,180)
# ogS = random.randint(0,255)
# ogV = random.randint(0,255)
# comp = complement((ogH, ogS, ogV))
# analog = analogous((int(ogH/2), ogS, ogV))
#
# print(ogH, ogS, ogV)
# while True:
#     visualize(analog[0], 'Lacc')
#     visualize(analog[1], 'Ltra')
#     visualize(analog[2], 'dom')
#     visualize(analog[3], 'Rtra')
#     visualize(analog[4], 'Racc')
#
#     #visualize(comp[0], 'DAcc')
#     #visualize(comp[1], 'D')
#     #visualize(comp[2], 'mid')
#     #visualize(comp[3], 'C')
#     #visualize(comp[4], 'CAcc')
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cv2.destroyAllWindows()