from math import sqrt
from typing import List, Tuple

from shapely import Polygon
from shapely.ops import nearest_points


# FIXME - optimize it!!!!

class ConditionOnTranslations:
    def __init__(self, kx, ky, c):
        self.kx = kx
        self.ky = ky
        self.c = c


def by_existing_separating_line(p1: Polygon, p2: Polygon) -> ConditionOnTranslations:
    if not p1.intersects(p2):
        return _single_for_not_intersected_polygons(p1, p2)
    if p1.touches(p2):
        return _single_for_touched_polygons(p1, p2)
    raise ValueError("p1 intersects p2")


def by_all_borders(p1: Polygon, p2: Polygon) -> List[ConditionOnTranslations]:
    directions = set()

    x, y = p1.exterior.coords.xy
    x_inner, y_inner = p1.centroid.xy
    for i in range(len(x) - 1):
        directions.add(
            _direction(
                x[i], y[i],
                x[i + 1], y[i + 1],
                x_inner[0], y_inner[0],
                True
            )
        )
    x, y = p2.exterior.coords.xy
    x_inner, y_inner = p2.centroid.xy
    for i in range(len(x) - 1):
        directions.add(
            _direction(
                x[i], y[i],
                x[i + 1], y[i + 1],
                x_inner[0], y_inner[0],
                False
            )
        )

    return [_to_condition(p1, p2, d[0], d[1]) for d in directions]


def _single_for_not_intersected_polygons(p1: Polygon, p2: Polygon) -> ConditionOnTranslations:
    pt1, pt2 = nearest_points(p1, p2)
    dx = pt2.x - pt1.x
    dy = pt2.y - pt1.y
    m = sqrt(dx * dx + dy * dy)
    dx /= m
    dy /= m
    return _to_condition(p1, p2, dx, dy)


def _single_for_touched_polygons(p1: Polygon, p2: Polygon) -> ConditionOnTranslations:
    for t in by_all_borders(p1, p2):
        if t.c <= 0:
            return t
    raise ValueError("precision issue")


def _to_condition(p1: Polygon, p2: Polygon, kx: float, ky: float) -> ConditionOnTranslations:
    return ConditionOnTranslations(kx, ky, _max_on_convex(p1, kx, ky)[0] - _min_on_convex(p2, kx, ky)[0])


def _direction(x1: float, y1: float,
               x2: float, y2: float,
               x_inner: float, y_inner: float,
               less: bool) -> Tuple[float, float]:
    kx = y1 - y2
    ky = x2 - x1
    m = sqrt(kx * kx + ky * ky)
    kx = kx / m
    ky = ky / m

    t1 = kx * x1 + ky * y1
    t_inner = kx * x_inner + ky * y_inner

    if (t_inner < t1) == less:
        return kx, ky
    return -kx, -ky


def _min_on_convex(p: Polygon, kx: float, ky: float) -> Tuple[float, float, float]:
    x, y = p.exterior.coords.xy
    ## FIXME - if len(x) > 10(?), use galloping
    return min([(kx * x[i] + ky * y[i], x[i], y[i]) for i in range(len(x))])


def _max_on_convex(p: Polygon, kx: float, ky: float) -> Tuple[float, float, float]:
    v, x, y = _min_on_convex(p, -kx, -ky)
    return -v, x, y
