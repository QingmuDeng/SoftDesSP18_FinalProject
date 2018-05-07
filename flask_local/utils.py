# import the necessary packages
import numpy as np
# import cv2
from PIL import ImageDraw, Image


def centroid_histogram(clt):
    """Grab the number of different clusters and create a histogram based
    on the number of pixels assigned to each cluster

    Args:
        clt (sklearn.cluster.Kmeans): a sklearn.cluster.Kmeans object that contains centroid
                                      locations and labels for each point
    Returns:
        hist (np.histogram): TODO
    """
    # create a histogram for clt.labels_ with the numbers of centroids as bin numbers
    (hist, _) = np.histogram(clt.labels_, bins=len(clt.cluster_centers_))

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist


def plot_colors(hist, centroids):
    """Initialize the bar chart representing the relative frequency of each of the colors.

    Args:
        hist (np.histogram): a histogram showing how many points are associated with
                             each centroid
    Returns:
        bar (np.arrary/image): a bar graph that display the centroid colors based on
                               the distribution in histogram
    """
    bar = np.zeros((120, 600, 3), dtype="uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    bar = Image.fromarray(bar)
    bar2 = ImageDraw.Draw(bar)
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 600)
        bar2.rectangle([int(startX), 0, int(endX), 120], fill=tuple(color.astype("uint8")), outline=tuple(color.astype("uint8")))
        # cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
        #               color.astype("uint8").tolist(), -1)
        startX = endX
    return bar
