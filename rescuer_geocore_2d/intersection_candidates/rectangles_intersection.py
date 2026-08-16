from typing import List

from rescuer_geocore_2d.intersection_candidates.interval_tree import build_minimal_interval_tree


def process_rect_intersection(rectangles: List[List[float]], callback):
    y_segments = []
    for rect in rectangles:
        y_segments.append((rect[1], rect[3]))

    root = build_minimal_interval_tree(y_segments)

    events = []
    for i in range(len(rectangles)):
        rect = rectangles[i]
        events.append((rect[0], 1, i))
        events.append((rect[2], 0, i))
    events.sort()

    for event in events:
        i = event[2]
        rect = rectangles[i]
        if event[1] == 0:
            root.remove_interval(rect[1], rect[3], i)
        else:
            root.callback_on_intersected(rect[1], rect[3], lambda x: callback(i, x))
            root.add_interval(rect[1], rect[3], i)
