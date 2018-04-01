"""Uses k means to determine the dominate colors in an image. Displays the results in a color histogram and saves the
RGB values in a csv file. """
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import utils
import cv2
import os, os.path
import csv
import numpy as np
import itertools

# create csv file with results
file = csv.writer(open('palettes.csv', 'wb'))
file.writerow(['image name', 'palette'])

# load image and convert from BGR to RBG
image_path = 'test2.jpg'
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# TESTING: show our image
# cv2.imshow('image',image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# reshape image to list of pixels
image = image.reshape((image.shape[0] * image.shape[1], 3))
# image = np.asarray(image)

# cluster the pixel intensities
clt = KMeans(n_clusters= 6)
clt.fit(image)

# build histogram of clusters and create a figure
# representing the number of pixels labeled to each color
hist = utils.centroid_histogram(clt)
bar = utils.plot_colors(hist, clt.cluster_centers_)

# extract the RGB pixel values
row = (image_path, [tuple(x) for x in bar])

# make a list of lists containing the RGB values for all the colors in the histogram
palette = []
for arr in list(row[1][0]):
    # print([arr[0], arr[1], arr[2]])
    palette.append([arr[0], arr[1], arr[2]])

# remove duplicates in the color list
# print(lst_palette)
palette = list(palette for palette,_ in itertools.groupby(palette))
# print(lst_palette)

# show our color bar
plt.figure()
plt.axis("off")
plt.imshow(bar)
plt.savefig("result2.png")
plt.show()
plt.close()

# write rbg values into csv file
file.writerow([
               row[0].encode('utf-8', 'ignore'),
               palette,
               ])


