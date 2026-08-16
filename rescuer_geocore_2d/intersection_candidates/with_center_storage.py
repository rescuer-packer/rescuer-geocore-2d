class _PairStorage:
    def __init__(self):
        self.cnt = 0
        self.pairs = []
        self.mapping = {}

    def add(self, ident, bound):
        self.pairs.append((bound, ident))
        self.mapping[ident] = self.cnt
        self.cnt += 1
        self._sift_left(self.cnt - 1)

    def remove(self, ident):
        p = self.mapping[ident]
        if p == self.cnt - 1:
            self._pop()
            return
        self._swap(p, self.cnt - 1)
        self._pop()
        self._sift_left(p)
        self._sift_right(p)


    def register_all(self, callback):
        for _, t in self.pairs:
            callback(t)

    def register_less(self, bound, callback):
        self._register_less_rec(0, bound, callback)

    def _register_less_rec(self, pos, bound, callback):
        if pos >= self.cnt:
            return
        p = self.pairs[pos]
        if p[0] >= bound:
            return
        callback(p[1])
        self._register_less_rec(2 * pos + 1, bound, callback)
        self._register_less_rec(2 * pos + 2, bound, callback)

    def _pop(self):
        p = self.pairs.pop()
        self.cnt -= 1
        del self.mapping[p[1]]

    def _sift_left(self, pos):
        while pos > 0:
            prev = (pos - 1) // 2
            if self.pairs[prev][0] <= self.pairs[pos][0]:
                return
            self._swap(pos, prev)
            pos = prev

    def _sift_right(self, pos):
        while True:
            pos_next, val_next = pos, self.pairs[pos][0]
            for p in [2 * pos + 1, 2 * pos + 2]:
                if p>=self.cnt:
                    break
                if self.pairs[p][0] < val_next:
                    pos_next = p
                    val_next = self.pairs[p][0]
            if pos_next == pos:
                return
            self._swap(pos, pos_next)
            pos = pos_next

    def _swap(self, p1, p2):
        self.pairs[p1], self.pairs[p2] = self.pairs[p2], self.pairs[p1]
        self.mapping[self.pairs[p1][1]] = p1
        self.mapping[self.pairs[p2][1]] = p2


class WithCenterStorage:
    def __init__(self):
        self.by_start = _PairStorage()
        self.by_end = _PairStorage()

    def add_segment(self, start, end, id):
        self.by_start.add(id, start)
        self.by_end.add(id, -end)

    def remove_segment(self, id):
        self.by_start.remove(id)
        self.by_end.remove(id)

    def register_all(self, callback):
        self.by_start.register_all(callback)

    def register_end_more(self, callback, val):
        self.by_end.register_less(-val, callback)

    def register_start_less(self, callback, val):
        self.by_start.register_less(val, callback)

