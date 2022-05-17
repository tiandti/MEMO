#!/usr/bin/env python3.9

"""Utilities needed by photo."""

# class Photo
#import imageio
#from PIL import Image
# from skimage import data
#from skimage import io
# from skimage import filters
#from matplotlib import pyplot as plt
#from skimage import exposure
#from skimage.color import rgb2gray
#from skimage.transform import swirl

# from skimage import data
#from skimage import segmentation
#from skimage import color
#from skimage.future import graph


import numpy as np


def weight_mean_color(graph, src, dst, n):
    """Merge nodes by recomputing mean color.

    The method expects that the mean color of `dst` is already computed.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    n : int
        A neighbor of `src` or `dst` or both.

    Returns
    -------
    data : dict
        A dictionary with the `"weight"` attribute set as the absolute
        difference of the mean color between node `dst` and `n`.
    """

    diff = graph.nodes[dst]['mean color'] - graph.nodes[n]['mean color']
    diff = np.linalg.norm(diff)
    return {'weight': diff}


def merge_mean_color(graph, src, dst):
    """Merge two nodes of a mean color distance graph.

    This method computes the mean color of `dst`.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    """
    graph.nodes[dst]['total color'] += graph.nodes[src]['total color']
    graph.nodes[dst]['pixel count'] += graph.nodes[src]['pixel count']
    graph.nodes[dst]['mean color'] = (graph.nodes[dst]['total color'] /
                                      graph.nodes[dst]['pixel count'])
