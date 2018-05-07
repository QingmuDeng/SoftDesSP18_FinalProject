import tensorflow as tf
import numpy as np
from ml_utils import ml_utils
import pickle
import multiprocessing as mp
from PIL import Image
import generate_palette as gp
from random import shuffle
import os, sys

tf.logging.set_verbosity(tf.logging.INFO)

def dense_fn(features, labels, mode):
    # Input Layer
    input_layer = tf.reshape(features['x'], [-1, 16])

    # Dense Layers
    dense1 = tf.layers.dense(inputs=input_layer, units=2048, activation=tf.nn.relu)
    dropout1 = tf.layers.dropout(inputs=dense1, rate=0.5, training=mode == tf.estimator.ModeKeys.TRAIN)

    dense2 = tf.layers.dense(inputs=dense1, units=2048, activation=tf.nn.relu)
    dropout2 = tf.layers.dropout(inputs=dense2, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    dense3 = tf.layers.dense(inputs=dropout2, units=2048, activation=tf.nn.relu)
    dropout3 = tf.layers.dropout(inputs=dense3, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    dense4 = tf.layers.dense(inputs=dropout3, units=2048, activation=tf.nn.relu)
    dropout4 = tf.layers.dropout(inputs=dense4, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    dense5 = tf.layers.dense(inputs=dropout4, units=2048, activation=tf.nn.relu)
    dropout5 = tf.layers.dropout(inputs=dense5, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    dense6 = tf.layers.dense(inputs=dropout5, units=2048, activation=tf.nn.relu)
    dropout6 = tf.layers.dropout(inputs=dense6, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    dense7 = tf.layers.dense(inputs=dropout6, units=2048, activation=tf.nn.relu)
    dropout7 = tf.layers.dropout(inputs=dense7, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    dense8 = tf.layers.dense(inputs=dropout7, units=2048, activation=tf.nn.relu)
    dropout8 = tf.layers.dropout(inputs=dense8, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    dense9 = tf.layers.dense(inputs=dropout8, units=1024, activation=tf.nn.relu)
    dropout9 = tf.layers.dropout(inputs=dense9, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    # Logits Layer
    logits = tf.layers.dense(inputs=dropout9, units=4)

    predictions = {
        "classes": tf.argmax(input=logits, axis=1),
        "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    # Loss Calculation
    onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=4)
    loss = tf.losses.softmax_cross_entropy(onehot_labels=onehot_labels, logits=logits)
    #Calculate Loss (for both TRAIN and EVAL modes)

    # Training
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
             loss = loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    # Evaluation
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            labels=labels, predictions=predictions["classes"])}
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)


def main(not_used):
    with open('dataset/processed.pckl', 'rb') as f:
        u = pickle._Unpickler(f)
        u.encoding = 'latin1'
        dataset = u.load()

    setlength = len(dataset)
    splitpoint = int(setlength * .8)
    shuffle(dataset)
    train = dataset[:splitpoint]
    evaluate = dataset[splitpoint:]

    train_data = np.asarray([data[0] for data in train]).astype(float)
    train_labels = np.asarray([data[1] for data in train], dtype=np.int32)

    eval_data = np.asarray([data[0] for data in evaluate]).astype(float)
    eval_labels = np.asarray([data[1] for data in evaluate], dtype=np.int32)

    # Create an Estimator
    dense_classifier = tf.estimator.Estimator(model_fn=dense_fn, model_dir='dataset/model_sess/')

    # Set up logging for predictions
    # Log the values in the softmax tensor with labels "probabilities"
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)

    # Train the model
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=16,
        num_epochs=None,
        shuffle=True
    )
    dense_classifier.train(
        input_fn=train_input_fn,
        steps=30000,
        hooks=[logging_hook]
    )

    # Evaluate the model
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_data},
        y=eval_labels,
        num_epochs=1,
        shuffle=False
    )
    eval_results = dense_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)


if __name__ == "__main__":
    with tf.device("/cpu:0"):
        tf.app.run()
