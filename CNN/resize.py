"""
Creates and pickles the dataset that is fed into the cnnImage script. Running make_dataset() creates the full dataset for testing on a supercomputer, running make_small_dataset() creates a smaller training/test set for testing the CNN on a PC.
"""
import cv2
import os, sys, glob, pickle
import numpy as np


def reshape_img(filename, dim):
    """
    Takes filepath, reads image, reshapes to a 64x64 image, reads all RGB values and converts to a 2d array, returns the array.
    filename: a str of the filepath to the image
    dim: an int of the desired dimension of the output image (64 in this case).
    returns: np array of dtype=float32.
    """
    #Initialize the numpy array
    img_array = np.zeros(shape=(dim*dim,3))
    dimension = (dim, dim)

    #Read the image
    image = cv2.imread(filename)

    #Convert image to 64x64 square
    resized = cv2.resize(image, dimension, interpolation = cv2.INTER_AREA)

    count = 0
    #Loops through every pixel, converts from BGR to RGB, normalizes range to be between 0-1 instead of 0-255, stores in a row of img_array.
    for length in range(dim):
        for height in range(dim):
            pixel = resized[length, height]
            blue, green, red = pixel[0], pixel[1], pixel[2]
            r, g ,b = red/255, green/255, blue/255
            img_array[count] = [r, g, b]
            count += 1
    return np.float32(img_array)

def flip_img(filename, dim):
    """
    Takes filepath, reads image, reshapes to a 64x64 image and flips horizontally over midline, reads all RGB values and converts to a 2D array.
    """
    #Initialize numpy array
    img_array = np.zeros(shape=(dim*dim, 3))
    dimension = (dim, dim)

    #Read the image
    load =cv2.imread(filename)

    #Convert image to 64x64 square
    resized = cv2.resize(load, dimension, interpolation = cv2.INTER_AREA)

    #Flip image
    image = cv2.flip(load, 1)

    count = 0
    #Loops through every pixel, converts from BGR to RGB, normalizes range to be between 0-1 instead of 0-255, stores in a row of img_array.
    for length in range(dim):
        for height in range(dim):
            pixel = resized[length, height]
            blue, green, red = pixel[0], pixel[1], pixel[2]
            r, g ,b = red/255, green/255, blue/255
            img_array[count] = [r, g, b]
            count += 1
    return np.float32(img_array)

def make_dataset(save_path='dataset/scaled_data'):
    """Takes the save_path as an argument.

    Returns the full dataset in 4 pickled files: train_img_array, train_label, test_img_array, testlabel, where each is a numpy array.

    train_img_array and test_img_array: contain RGB pixel values of every img in the dataset

    trainlabel and testlabel: contain the appropriate label for each image in the dataset stored as int32. 0=happiness, 1=sadness, 2=violence, 3=mysterious."""

    #Initialize the numpy arrays
    trainlabel= np.zeros(shape=(4000,1), dtype = 'int32')
    testlabel = np.zeros(shape=(2284,1), dtype='int32')
    train_img_array = np.zeros(shape=(4000,32*32, 3), dtype= 'float32')
    test_img_array = np.zeros(shape=(2284, 32*32, 3), dtype= 'float32')

    #Initialize the counters
    train_count = 0
    test_count = 0
    keywords = ['happiness', 'sadness', 'violence', 'mysterious']

    #Loop through the keywords, convert each image into a numpy matrix of pixel intensities, add result and corresponding label to the appropriate dataset array.
    for keyword in keywords:
        #Initialize counters to track distribution of training and test images per keyword.
        train_num_images = 0
        test_num_images = 0
        label = None
        print(keyword)

        #Loops through each image in the keyword folder
        for infile in glob.glob("dataset/"+keyword+"/*.jpg"):
            index = keywords.index(keyword)

            #Sorts first 500 images into training set, all others go to test set
            if train_num_images < 1000:
                train_img_array[train_count,:,:] = reshape_img(infile, 32)
                #print(train_img_array[train_count,:,:])
                trainlabel[train_count] = index
                #train_num_images += 1
                train_count += 1

                train_img_array[train_count,:,:] = flip_img(infile, 32)   #stores flipped image as np array
                trainlabel[train_count] = index
                train_num_images += 2
                train_count += 1
            else:
                test_img_array[test_count] = reshape_img(infile, 32)
                testlabel[test_count] = index
                #test_num_images +=1
                test_count += 1

                test_img_array[test_count,:,:] = flip_img(infile, 32)   #stores flipped image as np array
                testlabel[test_count] = index
                test_num_images +=2
                test_count += 1
        print(str(train_num_images), str(test_num_images))

    #Saves final arrays into files
    f = open('train_img_array.pckl', 'wb')
    pickle.dump(train_img_array, f)
    f.close()
    f2 = open('test_img_array.pckl', 'wb')
    pickle.dump(test_img_array, f2)
    f2.close()
    f3 = open('trainlabel.pckl', 'wb')
    pickle.dump(trainlabel, f3)
    f3.close()
    f4 = open('testlabel.pckl', 'wb')
    pickle.dump(testlabel, f4)
    f4.close()

def make_small_dataset(save_path='dataset/scaled_data'):
    trainlabel= np.zeros(shape=(200,1), dtype='int32')
    testlabel = np.zeros(shape=(100,1), dtype='int32')
    train_img_array = np.zeros(shape=(200,64*64, 3), dtype='float32')
    test_img_array = np.zeros(shape=(100, 64*64, 3), dtype='float32')
    train_count = 0
    test_count = 0
    keywords = ['happiness', 'sadness', 'violence', 'mysterious']

    #Loops through each keyword
    for keyword in keywords:
        count=0
        label = None
        print(keyword)

        #Loops through each image in the folder, converts to matrix, finds label, and adds to appropriate dataset
        for infile in glob.glob("dataset/"+keyword+"/*.jpg"):
            index = keywords.index(keyword)

            #Sorts first 50 into training set, next 25 into test, then moves on to next keyword
            if count < 50:
                train_img_array[train_count,:,:] = reshape_img(infile, 64)
                trainlabel[train_count] = index
                count += 1
                train_count += 1
            elif 50<=count<75:
                test_img_array[test_count] = reshape_img(infile, 64)
                testlabel[test_count] = index
                count += 1
                test_count += 1
            else:
                break
        print(str(train_count), str(test_count))

    #save the data
    f = open('train_img_array_smol.pckl', 'wb')
    pickle.dump(train_img_array, f)
    f.close()
    f2 = open('test_img_array_smol.pckl', 'wb')
    pickle.dump(test_img_array, f2)
    f2.close()
    f3 = open('trainlabel_smol.pckl', 'wb')
    pickle.dump(trainlabel, f3)
    f3.close()
    f4 = open('testlabel_smol.pckl', 'wb')
    pickle.dump(testlabel, f4)
    f4.close()


if __name__ == "__main__":
    #print(reshape_img("dataset/happiness/30631585.jpg", 64))
    make_dataset()
