import cv2
import numpy as np


def visualize(hsv):
    canvas = np.zeros((100, 100, 3), np.uint8)
    canvas[:, :] = hsv
    canvas = cv2.cvtColor(canvas, cv2.COLOR_HSV2BGR)
    cv2.imshow('canvas', canvas)


while True:
    visualize((160, 207, 225))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
