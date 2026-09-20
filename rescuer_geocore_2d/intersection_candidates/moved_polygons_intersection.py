from typing import List, Tuple

from shapely import Polygon

from rescuer_geocore_2d.intersection_candidates.rectangles_intersection import process_rect_intersection


def moved_polygons_intersection(polygons: List[Tuple[Polygon, int]], step: float, callback):
       big_polys = []
       bounds = []

       moves = [(step, step), (-step, step), (-step, -step),(step, -step)]

       for poly in polygons:
           p = _mink_sum(poly[0], moves)
           big_polys.append(p)
           bounds.append(p.bounds)

       def _inner_callback(i, j):
           if polygons[i][1] == polygons[j][1]:
               return
           if big_polys[i].intersects(big_polys[j]):
               if not big_polys[i].touches(big_polys[j]):
                   callback(i, j)

       process_rect_intersection(bounds, _inner_callback)




def _mink_sum(polygon: Polygon, moves: List[Tuple[float, float]]) -> Polygon:
    coords = list(polygon.exterior.coords)
    ls = []
    for p in coords:
        for m in moves:
            ls.append((p[0]+m[0], p[1]+m[1]))
    return Polygon(ls).convex_hull
