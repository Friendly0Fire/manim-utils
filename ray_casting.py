from manim import *
import numpy as np
from typing import NamedTuple, Union
from manim_utils.math import *
import shapely
import random


class CSegment(NamedTuple):
    p1: np.array
    p2: np.array

    def dir(self):
        return normalize(self.p2 - self.p1)


class CLine(NamedTuple):
    p1: np.array
    p2: np.array

    def dir(self):
        return normalize(self.p2 - self.p1)


class CRay(NamedTuple):
    o: np.array
    d: np.array

    def dir(self):
        return normalize(self.d)


CLinear = Union[CSegment, CLine, CRay]
Vector = np.array


def linear_intersection(
    a: Union[CSegment, CLine, CRay], b: Union[CSegment, CLine, CRay]
):
    (point11, point12, point21, point22) = (None, None, None, None)
    if isinstance(a, CRay):
        point11 = a.o
        point12 = a.o + a.d
    else:
        point11 = a.p1
        point12 = a.p2

    if isinstance(b, CRay):
        point21 = b.o
        point22 = b.o + b.d
    else:
        point21 = b.p1
        point22 = b.p2

    v1 = point21 - point11
    v2 = point12 - point11
    v3 = perp(point22 - point21)
    dot = np.dot(v2, v3)
    if abs(dot) < 1e-4:
        return None

    t1 = np.dot(v1, v3) / dot
    t2 = np.cross(v2[0:2], v1[0:2]) / dot

    if (isinstance(a, CRay) or isinstance(a, CSegment)) and t1 < 0:
        return None

    if isinstance(a, CSegment) and t1 > 1:
        return None

    if (isinstance(b, CRay) or isinstance(b, CSegment)) and t2 < 0:
        return None

    if isinstance(b, CSegment) and t2 > 1:
        return None

    return point11 + v2 * t1


def point_inside_polygon(point, vertices):
    point = shapely.geometry.Point(*point[0:2])
    polygon = shapely.geometry.polygon.Polygon([(v[0], v[1]) for v in vertices])
    return polygon.contains(point)


def reflect_from_surface(l: CLinear, vec):
    vec = normalize(vec)
    n = perp(l.dir())
    if np.dot(n, vec) > 0:
        n = -n
    return vec - 2 * np.dot(n, vec) * n


def normal_from_surface(l: CLinear, vec=None):
    n = perp(l.dir())
    if vec is not None and np.dot(n, vec) > 0:
        n = -n
    return n


def random_walk(direction: Vector, max_angle=TAU / 4, movement_range=[0.5, 1]):
    turnAngle = random.uniform(-max_angle, max_angle)
    movementLength = random.uniform(*movement_range)
    movement = rotate_vector(direction, turnAngle) * movementLength
    return movement