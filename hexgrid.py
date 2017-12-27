#!/usr/bin/env python

from elements import Elem


def mkCoords(sz):
    coords = []
    for i in range(-sz + 1, sz):
        for j in range(-sz + 1, sz):
            if abs(i + j) < sz:
                coords.append((i, j))
    return coords


# pointy hexgonal
def cartesian(coord):
    x, y = coord
    return x + 0.5 * y, 0.866 * y  # math.sqrt(3)/2 ~= 0.866


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
        self.cur_metal = Elem.lead
        for coord in mkCoords(size):
            self.elements[coord] = None

    def add_elem(self, coord, el):
        if self._in_grid(coord):
            self.elements[coord] = el

    def remove_elem(self, coord):
        if self._in_grid(coord):
            self.elements[coord] = None

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
                        #  don't check if is gold, call purge after rm it
                        self.cur_metal = metals[metals.index(el) + 1]
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
        for v in self.elements.values():
            if v is not None:
                return False
            return True

    def __eq__(self, g):
        return g.elements == self.elements

    def __hash__(self):
        return hash(frozenset(self.elements))
