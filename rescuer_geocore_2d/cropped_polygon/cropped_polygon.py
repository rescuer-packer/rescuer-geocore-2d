from typing import List

from shapely import Polygon
from shapely import affinity


def _subpoly(poly, ls):
    xx, xy = poly.exterior.coords.xy
    ans = []
    for i in ls:
        ans.append((xx[i], xy[i]))
    return Polygon(ans)


class CroppedPolygon:
    def __init__(self, convex: Polygon, crops: List[Polygon]):
        self.convex = convex
        self.crops = crops


class CroppedPolygonBuilder:
    def __init__(self, polygon: Polygon, crops: List[List[int]] = None):
        self.polygon = polygon
        self.crops = crops if crops is not None else []

    def build(self, x: float, y: float, angle: float, radians: bool) -> CroppedPolygon:
        polygon = affinity.translate(
            affinity.rotate(self.polygon, angle, (0, 0), use_radians=radians),
            x, y)
        if len(self.crops) == 0:
            return CroppedPolygon(polygon, [polygon])

        crops = [_subpoly(polygon, ls) for ls in self.crops]
        return CroppedPolygon(polygon.convex_hull, crops)
