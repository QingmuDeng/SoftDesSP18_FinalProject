import tensorflow as tf
import numpy as np
from ml_utils import ml_utils

tf.logging.set_verbosity(tf.logging.INFO)


def dense_fn(features, labels, mode):

    # Input Layer
    input_layer = tf.reshape(features['x'], [-1, 16])

    # Dense Layers
    dense1 = tf.layers.dense(inputs=input_layer, units=2048, activation=tf.nn.relu)
    dropout1 = tf.layers.dropout(inputs=dense1, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    dense2 = tf.layers.dense(inputs=dropout1, units=2048, activation=tf.nn.relu)
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
    dropout9 = tf.layers.dropout(inputs=dense8, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

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


def cluster_around(flattened_img, centroids):
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


def main(not_used):

    ML = ml_utils()
    ML.shuffle()
    ML.split()
    # Import data
    train_data = ML.tr_data
    train_labels = ML.tr_label
    eval_data = ML.eva_data
    eval_labels = ML.eva_data

    # Create an Estimator
    dense_classifier = tf.estimator.Estimator(model_fn=dense_fn, model_dir='dataset/color_model')

    # Set up logging for predictions
    # Log the values in the softmax tensor with labels "probabilities"
    tensors_to_log = {"probabilities": "softmax"}
    logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)

    # Train the model
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=50,
        num_epoch=None,
        shuffle=True
    )
    dense_classifier.train(
        input_fn=train_input_fn,
        steps=20000,
        hooks=[logging_hook]
    )

    # Evaluate the model
    eval_input_fn = tf.estimator.input.numpy_input_fn(
        x={"x": eval_data},
        y=eval_labels,
        num_epoch=1,
        shuffle=False
    )
    eval_results = dense_classifier.Evaluate(input_fn=eval_input_fn)


if __name__ == "__main__":
    tf.app.run()
