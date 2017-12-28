#!/usr/bin/env python

from copy import deepcopy
from elements import Elem as E
from itertools import combinations
import screen


_match_rules = set([
    (E.fire, E.fire),
    (E.water, E.water),
    (E.air, E.air),
    (E.earth, E.earth),
    (E.salt, E.salt),
    (E.salt, E.fire),
    (E.salt, E.water),
    (E.salt, E.air),
    (E.salt, E.earth),
    (E.mors, E.vitae),
    (E.quicksilver, E.lead),
    (E.quicksilver, E.tin),
    (E.quicksilver, E.iron),
    (E.quicksilver, E.copper),
    (E.quicksilver, E.silver),
    (E.quicksilver, E.gold)
])

match_rules = set()
for r1, r2 in _match_rules:
    match_rules.add((r1, r2))
    match_rules.add((r2, r1))
# single gold is a rule too


def score(comb):
    if comb[0] == E.vitae and comb[1] == E.mors:
        return 4
    if comb[1] == E.vitae and comb[0] == E.mors:
        return 4
    if comb[0] == E.quicksilver or comb[1] == E.quicksilver:
        return 3
    if comb[0] == E.salt or comb[1] == E.salt:
        return 2
    return 3

def prio_sort(moves):
    return sorted(moves, key=lambda x: score(x[2]), reverse=True)


def get_valid_moves(grid):
    valid_moves = []
    if len(grid.active) == 1:  # only gold left?
        for coord, el in grid.elements.items():
            if el is E.gold:
                return [(coord, coord, (E.gold, E.gold))]
        return []  # bug
    for x, y in combinations(grid.active, 2):
        comb = grid.elements[x], grid.elements[y]
        if comb in match_rules:
            valid_moves.append((x, y, comb))
    return prio_sort(valid_moves)

def solve(grid):
    seen = set()
    steps = {}
    how = None
    stack = [grid]
    while len(stack) != 0:
        cur_grid = stack.pop()
        if cur_grid in seen:
            continue
        seen.add(cur_grid)
        for x, y, _ in get_valid_moves(cur_grid):
            grid = deepcopy(cur_grid)
            grid.remove_elem(x)
            grid.remove_elem(y)
            grid.purge()
            steps[grid] = (x, y)
            stack.append(grid)
            if grid.win():
                return steps
    return steps


if __name__ == "__main__":
    g = screen.get_grid()
    print(solve(g))
