from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import tensorflow as tf
from PIL import Image
import os, sys, glob, pickle
import generate_palette as gp
from sklearn.cluster import KMeans


class ml_utils:
    def __init__(self, keywords=['happiness', 'sadness', 'violence', 'mysterious']):
        self.dataset = []
        self.length = None
        self.keywords = keywords
        self.train = []
        self.evaluate = []
        self.tr_data = []
        self.tr_label = []
        self.eva_data = []
        self.eva_label = []
        self.combined = None
        self.problems = []
        self.first_pass = True
        self.counter = 0
        self.shuffled = False

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
                # img = np.array(Image.open(infile))
                # img = np.reshape(img, (img.shape[0]*img.shape[1], 3))
                self.dataset.append((infile, label))

        self.length = len(self.dataset)
        f = open(save_path, 'wb')
        pickle.dump(self.dataset, f)
        f.close()

    def shuffle(self, save_path='dataset/data_with_label.pckl'):
        if not self.dataset:
            f = open(save_path, 'rb')
            self.dataset = pickle.load(f)
            f.close()
        np.random.shuffle(self.dataset)
        self.shuffled = True

    def split(self, tr_percent=.75):
        if not self.shuffled:
            self.shuffle()
        split_point = int(self.length * tr_percent)
        self.train = self.dataset[:split_point]
        self.tr_data = [each[0] for each in self.train]
        self.tr_label = [each[1] for each in self.train]
        self.evaluate = self.dataset[split_point:]
        self.eva_data = [each[0] for each in self.evaluate]
        self.eva_label = [each[1] for each in self.evaluate]

    def load_rgb(self, keyword='test'):
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
        f = open('dataset/store.pckl', 'wb')
        pickle.dump(self.combined, f)
        f.close()
        f = open('dataset/problem.pckl', 'wb')
        pickle.dump(self.problems, f)
        f.close()

    def load_RGBs(self):
        f = open('dataset/store.pckl', 'rb')
        self.combined = pickle.load(f)
        f.close()

    def complie_RGBs(self):
        for keyword in self.keywords:
            self.load_rgb(keyword)
        self.save_RGBs()

    def KMeans_cluster(self, centroid_num):
        clt = KMeans(n_clusters=centroid_num).fit(self.combined)
        print(clt.cluster_centers_)
        f = open('dataset/clt.pckl', 'wb')
        pickle.dump(clt, f)
        f.close()


if __name__ == '__main__':
