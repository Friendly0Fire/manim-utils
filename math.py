import numpy as np
import math


def perp(v):
    return np.array((-v[1], v[0], v[2]))


def clamp(x, minx, maxx):
    return min(max(x, minx), maxx)


def lerp(a, b, s):
    return a * (1 - s) + b * s


def vector_from_angle(t):
    return np.array([math.cos(t), math.sin(t), 0])