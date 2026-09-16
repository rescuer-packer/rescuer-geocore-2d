from typing import List

from shapely import Polygon
from shapely.ops import nearest_points

class ConditionOnTranslations:
    def __init__(self, kx, ky, c):
        self.kx = kx
        self.ky = ky
        self.c = c

def by_current_separating_line(p1: Polygon, p2: Polygon ) -> ConditionOnTranslations:
    if not p1.intersects(p2):
        return _single_for_not_intersected_polygons(p1, p2)
    if p1.touches(p2):
        return _single_for_touched_polygons(p1, p2)
    raise ValueError("p1 intersects p2")

def by_all_borders(s1: Polygon, s2: Polygon ) -> List[ConditionOnTranslations]:
    pass


def _single_for_not_intersected_polygons(p1: Polygon, p2: Polygon) -> ConditionOnTranslations:
    pt1, pt2 = nearest_points(p1, p2)
    pass

def _single_for_touched_polygons(p1: Polygon, p2: Polygon) -> ConditionOnTranslations:
    for t in  by_all_borders(p1, p2):
        if t.c <= 0:
            return t
    raise ValueError("precision issue")