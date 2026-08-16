from typing import List, Tuple

from rescuer_geocore_2d.intersection_candidates.with_center_storage import WithCenterStorage

_NO = 0
_LEFT = 1
_RIGHT = 2
_EACH = 3

class IntervalTree:
    def __init__(self, center: float, left: 'IntervalTree|None', right: 'IntervalTree|None'):
        self.center = center
        self.left = left
        self.right = right
        self.count = 0
        self.all = set()
        self.with_center = WithCenterStorage()

    def add_interval(self, start: float, end: float, id: int):
        self.count += 1
        self.all.add(id)
        if end<=self.center:
            self.left.add_interval(start, end, id)
        else:
            if start>=self.center:
                self.right.add_interval(start, end, id)
            else:
                self.with_center.add_segment(start, end, id)

    def remove_interval(self, start: float, end: float, id: int):
        self.count -= 1
        self.all.remove(id)
        if end <= self.center:
            self.left.remove_interval(start, end, id)
        else:
            if start >= self.center:
                self.right.remove_interval(start, end, id)
            else:
                self.with_center.remove_segment(id)

    def callback_on_intersected(self, start: float, end: float, callback, mode = _NO):
        if self.count == 0:
            return
        if mode == _EACH:
            for id in self.all:
                callback(id)
            return

        if end <= self.center:
            self.with_center.register_start_less(callback, end)
            self.left.callback_on_intersected(start, end, callback, mode)
            return

        if start >= self.center:
            self.with_center.register_end_more(callback, start)
            self.right.callback_on_intersected(start, end, callback, mode)
            return

        ## self.center between start and end
        self.with_center.register_all(callback)
        self.left.callback_on_intersected(start, end, callback, mode|_RIGHT)
        self.right.callback_on_intersected(start, end, callback, mode|_LEFT)



_zero_tree_elem = IntervalTree(0, None, None)

def _build_interval_tree(arr: List[float])-> IntervalTree:
    if len(arr) == 0:
        return _zero_tree_elem
    c = len(arr)//2
    return IntervalTree(arr[c], _build_interval_tree(arr[:c]), _build_interval_tree(arr[c+1:]))


def build_minimal_interval_tree(segments: List[Tuple[float, float]]) -> IntervalTree:
    segments.sort()
    e_segments = []
    for start, end in segments:
        e_segments.append((end, start))
    e_segments.sort()
    points = []
    max_covered = segments[0][0] - 1

    pos_s = 0
    pos_e = 0
    N = len(segments)
    while pos_e < N:
        if e_segments[pos_e][0] <= max_covered:
            pos_e = 1
            continue
        end_point = e_segments[pos_e][0]
        pos_e += 1
        while pos_s < N and segments[pos_s][0] < end_point:
            max_covered = segments[pos_s][0]
            pos_s += 1
        points.append((max_covered+ end_point)/2)
    return _build_interval_tree(points)


