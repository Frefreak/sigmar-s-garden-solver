#!/usr/bin/env python

from copy import deepcopy
import visual
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


def score(grid, comb):
    if comb[0] == E.quicksilver or comb[1] == E.quicksilver:
        return 5
    if comb[0] == E.vitae or comb[1] == E.vitae:
        return 4
    if comb[0] == E.salt or comb[1] == E.salt:
        return 2
    if comb[0] == E.salt and comb[1] == E.salt:
        return 0
    if comb[0] == comb[1] and comb[0] in \
            [E.fire, E.earth, E.water, E.air]:
        if grid.nums[comb[0]] == 2:
            print('gold move')
            return 10
    return 3

def prio_sort(grid, moves):
    return sorted(moves, key=lambda x: score(grid, x[2]), reverse=True)


def get_valid_moves(grid):
    valid_moves = []
    if grid.rem == 1:
        for coord, el in grid.elements.items():
            if el is E.gold:
                return [(coord, coord, (E.gold, E.gold))]
        return []  # bug
    for x, y in combinations(grid.active, 2):
        comb = grid.elements[x], grid.elements[y]
        if comb in match_rules:
            valid_moves.append((x, y, comb))
    return prio_sort(grid, valid_moves)
    #  return valid_moves


def impossible(grid):
    if grid.nums[E.salt] == 0:
        if grid.nums[E.fire] % 2 or \
                grid.nums[E.earth] % 2 or \
                grid.nums[E.water] % 2 or \
                grid.nums[E.air] % 2:
            return True
    return False

def solve(grid):
    seen = set()
    seen.add(grid)
    steps = {}
    stack = [grid]
    cnt = 0
    while len(stack) != 0:
        cur_grid = stack.pop()
        cnt += 1
        print(cnt, cur_grid.rem, len(stack), len(seen))
        if impossible(grid):
            continue
        for x, y, _ in get_valid_moves(cur_grid):
            ngrid = deepcopy(cur_grid)
            ngrid.remove_elem(x)
            ngrid.remove_elem(y)
            ngrid.purge()
            if ngrid in seen:
                continue
            steps[ngrid] = ((x, y), cur_grid)
            stack.append(ngrid)
            seen.add(ngrid)
            if ngrid.win():
                return steps
    print('failed')
    return steps


if __name__ == "__main__":
    g = screen.get_grid()
    visual.draw_grid(g)
    print('start')
    print(solve(g))
