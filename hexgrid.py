#!/usr/bin/env python

import math
from collections import defaultdict
from elements import Elem, metal_value
from hashlib import md5


def mkCoords(sz):
    coords = []
    for i in range(-sz + 1, sz):
        for j in range(-sz + 1, sz):
            if abs(i + j) < sz:
                coords.append((i, j))
    return coords


# pointy hexgonal
def cartesian(coord, scale=1.):
    x, y = coord
    return (x + 0.5 * y) * scale, (math.sqrt(3) / 2 * y) * scale


neighbour_offset = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]


metals = [Elem.lead, Elem.tin, Elem.iron, Elem.copper, Elem.silver, Elem.gold]
metal_set = set(metals)


def is_metal(el):
    return el in metal_set


def neighbours(coord):
    nbs = []
    cx, cy = coord
    for x, y in neighbour_offset:
        nbs.append((cx + x, cy + y))
    return nbs


class HexGrid():
    def __init__(self, size):
        self.size = size
        self.elements = {}
        self.active = set()
        self.cur_metal = Elem.gold
        self.rem = 0
        self.nums = defaultdict(int)
        self.gold_coord = None
        for coord in mkCoords(size):
            self.elements[coord] = None

    def add_elem(self, coord, el):
        if self._in_grid(coord):
            if self.elements[coord] is None and el is not None:
                self.rem += 1
                self.elements[coord] = el
                self.nums[el] += 1
                if is_metal(el):
                    if metal_value[el] < metal_value[self.cur_metal]:
                        self.cur_metal = el
                if el is Elem.gold:
                    self.gold_coord = coord

    def remove_elem(self, coord):
        if self._in_grid(coord):
            el = self.elements[coord]
            if el is not None:
                self.rem -= 1
                self.elements[coord] = None
                self.nums[el] -= 1
                if is_metal(el):
                    if el is Elem.gold:
                        self.gold_coord = None
                    else:
                        self.cur_metal = \
                            metals[metals.index(self.cur_metal) + 1]

    def mk_active(self, coord):
        if self._in_grid(coord):
            self.active.add(coord)

    def _in_grid(self, coord):
        return coord in self.elements.keys()

    def purge(self):
        self.active = set()
        for coord, el in self.elements.items():
            if el is not None and self.is_active(coord):
                if is_metal(el):
                    if el == self.cur_metal:
                        self.active.add(coord)
                else:
                    self.active.add(coord)

    def _empty(self, coord):
        return not self._in_grid(coord) or self.elements[coord] is None

    def is_active(self, coord):
        nbs = neighbours(coord)
        for i in range(6):
            # TODO: optimize this if necessary
            if self._empty(nbs[i]) and self._empty(nbs[(i + 1) % 6]) and \
                    self._empty(nbs[(i + 2) % 6]):
                return True
        return False

    def win(self):
        return self.rem == 0

    def __hash__(self):
        h = md5(repr(sorted(self.elements.items())).encode())
        return int(h.hexdigest(), 16)
