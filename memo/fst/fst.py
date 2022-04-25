#!/usr/bin/env python3.9

"""Fast style transfer."""

import os
# Disable tensorflow logging to stdout
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from memo.fst import transform
import tensorflow as tf
import numpy as np


# get img_shape
# image: ImageIo bytes
# checkpoint_dir: Checkpoint directory or path
def fst(image, checkpoint_dir):
    """Get img_shape."""
    if image is None or checkpoint_dir is None:
        return None

    device_t = '/gpu:0'
    img_shape = image.shape

    g = tf.Graph()
    batch_size = 1
    soft_config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
    soft_config.gpu_options.allow_growth = True
    with g.as_default(), g.device(device_t), \
            tf.compat.v1.Session(config=soft_config) as sess:
        batch_shape = (batch_size,) + img_shape
        img_placeholder = tf.compat.v1.placeholder(tf.float32, shape=batch_shape, name='img_placeholder')

        preds = transform.net(img_placeholder)
        saver = tf.compat.v1.train.Saver()
        if os.path.isdir(checkpoint_dir):
            ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
            else:
                raise Exception("No checkpoint found...")
        else:
            saver.restore(sess, checkpoint_dir)

        X = np.zeros(batch_shape, dtype=np.float32)
        X[0] = image

        _preds = sess.run(preds, feed_dict={img_placeholder: X})
        img = np.clip(_preds[0], 0, 255).astype(np.uint8)
        return img
    return None


if __name__ == '__main__':
    import sys
    import imageio

    image_in = None
    checkpoint = None
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        image_in = imageio.imread(filepath, pilmode='RGB')
        print(f"Read '{filepath}'")
    if len(sys.argv) == 3:
        checkpoint = sys.argv[2]
    image_out = fst(image_in, "models/scream.ckpt")
    if image_out is not None:
        imageio.imwrite("output/out.jpg", image_out)
        print("Wrote 'output/out.jpg'")
