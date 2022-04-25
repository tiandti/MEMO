#!/usr/bin/env python3.9

"""Fast style transfer."""

import os
# Disable tensorflow logging to stdout
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from argparse import ArgumentParser
from collections import defaultdict
from utils import save_img, get_img, exists, list_files
import transform
import tensorflow as tf
import numpy as np


# get img_shape
def fst(data_in, checkpoint_dir, device_t='/gpu:0', batch_size=1):
    """Get img_shape."""
    is_paths = type(data_in[0]) == str
    if is_paths:
        img_shape = get_img(data_in[0]).shape

    g = tf.Graph()
    batch_size = 1
    # curr_num = 0
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

        num_iters = 1
        for i in range(num_iters):
            pos = i * batch_size
            if is_paths:
                curr_batch_in = data_in[pos:pos + batch_size]
                X = np.zeros(batch_shape, dtype=np.float32)
                for j, path_in in enumerate(curr_batch_in):
                    img = get_img(path_in)
                    assert img.shape == img_shape, \
                        'Images have different dimensions. ' +  \
                        'Resize images or use --allow-different-dimensions.'
                    X[j] = img
            else:
                X = data_in[pos:pos + batch_size]

            _preds = sess.run(preds, feed_dict={img_placeholder: X})
            img = np.clip(_preds[0], 0, 255).astype(np.uint8)
            return img
    return None


if __name__ == '__main__':
    import imageio
    img = fst(["media/hockney.png"], "models/scream.ckpt")
    imageio.imwrite("output/out.jpg", img)
