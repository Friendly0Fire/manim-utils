import numpy as np
import math
import manim_utils as mu
from manim import *


def BlinnPhong(l, v, alpha):
    n = np.array([0, 1, 0])
    h = normalize(l + v)
    ndoth = np.dot(n, h)
    ndotl = np.dot(n, l)
    return mu.math.clamp(ndotl, 0, 1) * 0.5 + math.pow(
        mu.math.clamp(ndoth, 0, 1), alpha
    )


def Lambert(l, n=np.array([0, 1, 0])):
    return np.dot(n, l)