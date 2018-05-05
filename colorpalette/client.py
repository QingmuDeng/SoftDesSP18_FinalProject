'''
Send JPEG image to tensorflow_model_server loaded with GAN model.

Hint: the code has been compiled together with TensorFlow serving
and not locally. The client is called in the TensorFlow Docker container
'''

import time
from PIL import Image
import numpy as np
import generate_palette as gp
from argparse import ArgumentParser
import pickle

# Communication to TensorFlow server via gRPC
from grpc.beta import implementations
import tensorflow as tf

# TensorFlow serving stuff to send messages
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from tensorflow.contrib.util import make_tensor_proto


def parse_args():
    parser = ArgumentParser(description="Request a TensorFlow server for a prediction on the image")
    parser.add_argument("-s", "--server",
                        dest="server",
                        default='172.17.0.2:9000',
                        help="prediction service host:port")
    parser.add_argument("-i", "--image",
                        dest="image",
                        default="",
                        help="path to image in JPEG format",)
    args = parser.parse_args()

    host, port = args.server.split(':')

    return host, port, args.image


def load_image(path, centers):
    """Given the list of data to be used, return a list of a nest list of
    16 percentages for the percentages of pixels that is the closest to
    each cluster center

    Returns: a 2D list of percentage

    Arguments:
        paths (list): a list of path to the datasets
        centroids (list): a list of cluster centers
    """

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
    image = np.array(Image.open(path))

    # resize the image to a lower dimension for less computing time
    image = gp.edit_image(image)
    cluster = cluster_around(image, centers)
    cluster = tf.convert_to_tensor([v for _, v in cluster.items()], dtype=tf.float32)

    return cluster


def main():
    with open('dataset/clt16.pckl', 'rb') as f:
        u = pickle._Unpickler(f)
        u.encoding = 'latin1'
        centers = u.load()
    # parse command line arguments
    host, port, image = parse_args()

    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

    # Send request
    with open(image, 'rb') as f:
        # See prediction_service.proto for gRPC request/response details.
        data = pickle.load(f)
        data = tf.convert_to_tensor(data, dtype=tf.float32)
        start = time.time()

        request = predict_pb2.PredictRequest()

        # Call GAN model to make prediction on the image
        request.model_spec.name = 'dense'
        request.model_spec.signature_name = 'predict_clusters'
        request.inputs['cluster'].CopyFrom(make_tensor_proto(data, shape=[1]))

        result = stub.Predict(request, 60.0)  # 60 secs timeout

        end = time.time()
        time_diff = end - start

        print(result)
        print('time elapased: {}'.format(time_diff))


if __name__ == '__main__':
    main()
