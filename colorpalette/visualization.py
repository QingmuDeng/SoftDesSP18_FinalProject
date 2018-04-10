import cv2
import numpy as np


def visualize(hsv):
    canvas = np.zeros((100, 100, 3), np.uint8)
    canvas[:, :] = hsv
    canvas = cv2.cvtColor(canvas, cv2.COLOR_HSV2BGR)
    cv2.imshow('canvas', canvas)


visualize((160, 207, 225))
cv2.waitKey(0)
cv2.destroyAllWindows()
