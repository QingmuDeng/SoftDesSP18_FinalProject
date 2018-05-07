from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import tensorflow as tf
from PIL import Image
import os, sys, glob, pickle
import generate_palette as gp
import multiprocessing as mp



class ml_utils():
    """This class is a utility class for vector quantization method.
    It provides loading the pixel values from datasets and running
    K means Clustering through them to find a set of center to use.
    """
    def __init__(self, keywords=['happiness', 'sadness', 'violence', 'mysterious']):
        self.dataset = []
        self.length = None
        self.keywords = keywords
        self.combined = None

    def make_dataset(self, save_path='dataset/data_with_label.pckl'):
        for keyword in self.keywords:
            label = None
            print(keyword)
            if keyword == self.keywords[0]:
                label = 0
            elif keyword == self.keywords[1]:
                label = 1
            elif keyword == self.keywords[2]:
                label = 2
            elif keyword == self.keywords[3]:
                label = 3
            for infile in glob.glob("dataset/"+keyword+"/*.jpg"):
                file, ext = os.path.splitext(infile)
                # upload_imgs = np.array(Image.open(infile))
                # upload_imgs = np.reshape(upload_imgs, (upload_imgs.shape[0]*upload_imgs.shape[1], 3))
                self.dataset.append((infile, label))

        self.length = len(self.dataset)
        f = open(save_path, 'wb')
        pickle.dump(self.dataset, f)
        f.close()

    def load_rgb(self, keyword='test'):
        """load the RGB values of one images in provided keywords for K
        Mean Clustering

        :param keyword: the keywords to load pixel values from
        :return self.combined.shape: the dimension of the variable with all the RGBs
        """
        for infile in glob.glob("dataset/"+keyword+"/*.jpg"):
            file, ext = os.path.splitext(infile)
            try:
                img = np.array(Image.open(infile))
            except:
                self.problems.append(infile)
                continue
            try:
                if img.shape[2] != 3:
                    self.problems.append(infile)
                    continue
            except:
                self.problems.append(infile)
                continue
            downsized_img = np.asarray(gp.edit_image(img))
            # print('new size', downsized_img.shape)
            if self.first_pass:
                self.combined = downsized_img
                self.first_pass = False
            else:
                self.combined = np.concatenate((self.combined, downsized_img))
            self.counter += 1
            print(self.counter)
        return self.combined.shape

    def save_RGBs(self):
        """save the loaded RGB values to a Pickle file"""
        f = open('dataset/store.pckl', 'wb')
        pickle.dump(self.combined, f)
        f.close()
        f = open('dataset/problem.pckl', 'wb')
        pickle.dump(self.problems, f)
        f.close()

    def load_RGBs(self):
        """load RGB values from a Pickle file"""
        f = open('dataset/store.pckl', 'rb')
        self.combined = pickle.load(f)
        f.close()

    def complie_RGBs(self):
        """load the RGB values of all the images in provided keywords for K
        Mean Clustering"""
        for keyword in self.keywords:
            self.load_rgb(keyword)
        self.save_RGBs()

    def KMeans_cluster(self, centroid_num):
        """K Means Clustering over all the RGB values to generate center"""
        input_fn = lambda: tf.train.limit_epochs(tf.convert_to_tensor(self.combined, dtype=tf.float32), num_epochs=1)
        kmeans = tf.contrib.factorization.KMeansClustering(num_clusters=centroid_num)
        kmeans.train(input_fn=input_fn)
        clt = kmeans.cluster_centers()
        print(clt)
        f = open('dataset/clt.pckl', 'wb')
        pickle.dump(clt, f)
        f.close()

    def load_image_mp(self, paths, centroids):
        """Given the list of data to be used, return a list of a nest list of
        16 percentages for the percentages of pixels that is the closest to
        each cluster center

        Returns: a 2D list of percentage

        Arguments:
            paths (list): a list of path to the datasets
            centroids (list): a list of cluster centers
        """

        # Define an multiprocessing output queue
        output = mp.Queue()
        img_data = []
        data_len = len(paths)

        def load_from_path(path, centroids, pos, output):
            def cluster_around(flattened_img, centroids):
                """Given a reshaped 2d numpy arrary of size n*3, this function
                loops through each element in the 2d numpy array and each cluster
                center, finds which cluster center is closest to that element, and
                add one to the value of the element in a dictionary with the cluster
                center as its key

                Returns: a normalized dictionary with each key being a cluster center

                Arguments:
                    paths (list): a list of path to the datasets
                    centroids (list): a list of cluster centers
                """
                cluster = dict((tuple(centroid), 0) for centroid in centroids)
                total = float(len(flattened_img))
                for i in flattened_img:
                    temp = 0
                    first_pass = True
                    which_centroid = None
                    for centroid in centroids:
                        dist = np.linalg.norm((i-centroid))
                        if first_pass:
                            which_centroid = centroid
                            temp = dist
                            first_pass = False
                        elif temp > dist:
                            which_centroid = centroid
                            temp = dist
                    cluster[tuple(which_centroid)] += 1
                cluster = dict((k, v/total) for k, v in cluster.items())
                return cluster
            # Read images with pillow and turn then into more general purpose
            # numpy arrays
            img = np.array(Image.open(+str(path)))

            # resize the image to a lower dimension for less computing time
            img = gp.edit_image(img)
            cluster = cluster_around(img, centroids)
            cluster = [v for _, v in cluster.items()]
            output.put((pos, cluster))

        times_to_run = 0
        last_iter = data_len
        counter = 0
        result = None
        if data_len > 300:
            times_to_run = int(data_len / 300)
            last_iter = int(data_len%100)

        for i in range(times_to_run):
            # Setup a list of processes that we want to run
            processes = [mp.Process(target=load_from_path, args=(paths[i+counter], centroids, i+counter, output)) for i in range(300)]
            counter += 300
            # Run processes
            for p in processes:
                p.start()

            # Exit the completed processes
            for p in processes:
                p.join()

            result = [output.get() for p in processes]
            print('successfully run')
            result.sort()
            print('successfully sorted')
            result = [r[1] for r in result]
            img_data.extend(result)

        # Setup a list of processes that we want to run
        processes = [mp.Process(target=load_from_path, args=(paths[i+counter], centroids, i+counter, output)) for i in range(last_iter)]
        counter += 300
        # Run processes
        for p in processes:
            p.start()

        # Exit the completed processes
        for p in processes:
            p.join()

        result = [output.get() for p in processes]
        print('successfully run')
        result.sort()
        print('successfully sorted')
        result = [r[1] for r in result]
        img_data.extend(result)

        return img_data


if __name__ == '__main__':
    ML = ml_utils()
    ML.load_RGBs()
    ML.KMeans_cluster(16)
