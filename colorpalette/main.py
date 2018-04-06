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

# show our image
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
# print bar

# extract the RGB pixel values and remove duplicates
color_palette = utils.plot_colors(hist, clt.cluster_centers_)
# print color_palette
row = (image_path, [tuple(x) for x in color_palette])

lst_palette = []
for arr in list(row[1][0]):
    # print([arr[0], arr[1], arr[2]])
    lst_palette.append([arr[0], arr[1], arr[2]])

print(lst_palette)
lst_palette = list(lst_palette for lst_palette,_ in itertools.groupby(lst_palette))
print(lst_palette)
# print row

# print row[0]
# print row[1]


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
               lst_palette,
               ])


