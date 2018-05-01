from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Imports
import numpy as np
import tensorflow as tf
import pickle
import resize

tf.logging.set_verbosity(tf.logging.INFO)

def cnn_model_fn(features, labels, mode):
    """Model function for CNN"""
    #Input Layer
    input_layer = tf.reshape(features["x"], [-1, 32, 32, 3])

    #Convolutional Layer #1
    conv1 = tf.layers.conv2d(inputs = input_layer, filters=32,
                            kernel_size=[10,10], padding='same', activation=tf.nn.relu)
    #Pooling Layer #1
    pool1 = tf.layers.max_pooling2d(inputs = conv1, pool_size=[2,2],strides=2)

    #Convolutional Layer #2 and Pooling Layer#2
    conv2 = tf.layers.conv2d(inputs=pool1, filters=64, kernel_size=[10,10], padding='same', activation=tf.nn.relu)
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2,2], strides=2)

    #Convolutional Layer #3 and Pooling Layer#3
    conv3 = tf.layers.conv2d(inputs=pool2, filters=32, kernel_size=[10,10], padding='same', activation=tf.nn.relu)
    pool3 = tf.layers.max_pooling2d(inputs=conv3, pool_size=[2,2], strides=2)

    #Convolutional Layer #4 and Pooling Layer#4
    conv4 = tf.layers.conv2d(inputs=pool3, filters=32, kernel_size=[10,10], padding='same', activation=tf.nn.relu)
    pool4 = tf.layers.max_pooling2d(inputs=conv4, pool_size=[2,2], strides=2)

    # #Convolutional Layer #5 and Pooling Layer#5
    # conv5 = tf.layers.conv2d(inputs=pool4, filters=32, kernel_size=[10,10], padding='same', activation=tf.nn.relu)
    # pool5 = tf.layers.max_pooling2d(inputs=conv5, pool_size=[2,2], strides=2)

    #Dense Layer
    pool5_flat = tf.reshape(pool4, [-1, 2*2*32])
    dense = tf.layers.dense(inputs=pool5_flat, units=1024, activation=tf.nn.relu)
    dropout = tf.layers.dropout(inputs=dense, rate=0.5, training=mode == tf.estimator.ModeKeys.TRAIN)

    #Logits Layer
    logits = tf.layers.dense(inputs=dropout, units=4)

    predictions = {
        #Generate predictions (for PREDICT and EVAL mode)
        "classes": tf.argmax(input=logits, axis=1),
        #Add 'softmax_tensor' to the graph. It is used for PREDICT and by the 'logging_hook'.
        "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    #Calculate Loss (for both TRAIN and EVAL modes)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    #Configure the Training Op (for TRAIN mode)
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer = optimizer.minimize(loss=loss, global_step = tf.train.get_global_step())
        eval_metric = {"accuracy": tf.metrics.accuracy(labels=labels, predictions=predictions["classes"])}
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op, eval_metric_ops=eval_metric)

    #Add evaluation metrics (for EVAL mode)
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(labels=labels, predictions=predictions["classes"])}
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

def run_model(unused_argv):
    #Load training and eval database
    #mnist = tf.contrib.learn.datasets.load_dataset("mnist")

    #import dataset
    f = open('train_img_array.pckl', 'rb')
    train_data = pickle.load(f) #Returns np.array
    f.close()

    f1 = open('trainlabel.pckl', 'rb')
    train_labels = pickle.load(f1)
    f1.close()

    f2 = open('test_img_array.pckl', 'rb')
    eval_data = pickle.load(f2) #Returns np.array
    f2.close()

    f3 = open('testlabel.pckl', 'rb')
    eval_labels = pickle.load(f3)
    f3.close()

    #Create the estimator
    sentiment_classifier =tf.estimator.Estimator(model_fn=cnn_model_fn, model_dir="imgsent_convnet_model")

    #Set up logging for predictions
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)

    #Train the model
    train_input_fn =tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=50,
        num_epochs=None,
        shuffle=True)
    sentiment_classifier.train(
        input_fn=train_input_fn,
        steps=8000,
        hooks=[logging_hook])

    #Evaluate the model and print results
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_data},
        y=eval_labels,
        num_epochs=1,
        shuffle=False)
    eval_results = sentiment_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)

def main(_):
    with tf.Graph().as_default():
        #Create placeholder image for future user input
        serialized_tf_example = tf.placeholder(tf.string, name='input_image')
        feature_configs ={'image/encoded':tf.FixedLenFeature(shape=[], dtype=tf.string), }

        tf_example = tf.parse_example(serialzed_tf_example, feature_configs)

        jpegs = tf_example['image/encoded']
        images = tf.map_fn(preprocess_image, jpegs, dtype=tf.float32)
        images = tf.squeeze(images, [0])

        #Create CNN model TODO check inputs. Needs to take in image
        CNN = run_model()

        #Create saver to restore from checkpoints
        saver = tf.train.Saver()

        with tf.Session as sess:
            #Restore the model from last checkpoints
            ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
            saver.resttore(sess, ckpt.model_checkpoint_path)

            #Recreate export directory
            export_path = os.path.join(
                tf.compat.as_bytes(FLAGS.output_dir), tf.compat.as_bytes(str(FLAGS.model_version)))
            if os.path.exists(export_path):
                shutil.rmtree(export_path)

            #Create the model builder
            builder = tf.saved_model.builder.SavedModelBuilder(export_path)

            #Create tensors info
            predict_tensor_inputs_info = tf.saved_model.utils.build_tensor_info(jpegs)
            predict_tensor_scores_info = tf.saved_model.utils.build_tensor_info(
                net.discriminator_out)

            #build prediction signature
            prediction_signature = (
                tf.saved_model.signature_def_utils.build_signature_def(
                    inputs={'images': predict_tensor_inputs_info},
                    outputs={'scores': predict_tensor_scores_info},
                    method_name = tf.saved_model.signature_constants.PREDICT_METHOD_NAME
                )
            )

            #save the model
            legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')
            builder.add_meta_graph_and_variables(
                sess, [tf.saved_model.tag_constants.SERVING],
                signature_def_map={
                    'predict_images': prediction_signature
                },
                legacy_init_op = legacy_init_op)

            builder.save()

        print("Successfully exported CNN model version '{}' into '{}'".format(
            FLAGS.model_version, FLAGS.output_dir))

def preprocess_image(image_buffer):
    """
    Preprocess JPEG encoded bytes to a 3D float Tensor and rescales it so that pixels are in a range of [0,1]

    :param image_buffer: Buffer that contains JPEG image
    :return: 4D image tensor (1, width, height, channels) with pixels scaled to [0,1]. First dimension is batch size (1 in this case)
    """

    #Decode string as an RGB jpeg. Note that height and width of img is set dynamically byt this method so dimensions of the image are unknown
    #TODO what format does the website give the image in? Can I use resize.py instead of tf stuff to make sure the dimensions are right?
    image = tf.image_decode_jpeg(image_buffer, channels=3)

    #Convert pixel values to float32 between [0,1]
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)

    #expand image array to include batch size
    image = tf.expand_dims(image, 0)

    return image

if __name__ == "__main__":
  tf.app.run()
