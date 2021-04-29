from manim import *
import numpy as np
from typing import NamedTuple, Union
from manim_utils.math import *
import shapely


class CSegment(NamedTuple):
    p1: np.array
    p2: np.array


class CLine(NamedTuple):
    p1: np.array
    p2: np.array


class CRay(NamedTuple):
    o: np.array
    d: np.array


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