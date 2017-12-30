#!/usr/bin/env python

from copy import deepcopy
import visual
from elements import Elem as E
from itertools import combinations
import numpy as np
import hexgrid
#  import screen


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


def score(grid, comb_):
    c1, c2, comb = comb_
    #  for nb in hexgrid.neighbours(c1) + hexgrid.neighbours(c2):
        #  if grid._in_grid(nb) and grid.elements[nb] == grid.cur_metal:
            #  return 7
        #  if grid._in_grid(nb) and grid.elements[nb] in hexgrid.metal_set:
            #  return 6
    #  if comb[0] == E.quicksilver or comb[1] == E.quicksilver:
        #  return 7
    #  if comb[0] == E.vitae or comb[1] == E.vitae:
        #  return 4
    #  if comb[0] == E.salt or comb[1] == E.salt:
        #  return 2
    #  if comb[0] == E.salt and comb[1] == E.salt:
        #  return 0
    if comb[0] == comb[1] and comb[0] in \
            [E.fire, E.earth, E.water, E.air]:
        if grid.nums[comb[0]] == 2:
            return 20
    s = 0
    for nb in set(hexgrid.neighbours(c1) + hexgrid.neighbours(c2)):
        if grid._in_grid(nb) and grid.elements[nb] is not None \
                and nb not in grid.active:
            s += 1
    return s

def prio_sort(grid, moves):
    return sorted(moves, key=lambda x: score(grid, x), reverse=True)


def get_valid_moves(grid):
    valid_moves = []
    if grid.gold_coord in grid.active:  # gold exposed, click !
        return [(grid.gold_coord, grid.gold_coord, (E.gold, E.gold))]
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
    result = dfs(grid, steps, seen, 0)
    return result, steps

def dfs(g, steps, seen, depth):
    #  print(g.rem)
    print(depth)
    #  visual.draw_grid(g)
    if impossible(g):
        return False
    for x, y, _ in get_valid_moves(g):
        #  prev = deepcopy(g)
        elx = g.elements[x]
        ely = g.elements[y]
        g.remove_elem(x)
        g.remove_elem(y)
        g.purge()
        if g in seen:
            g.add_elem(x, elx)
            g.add_elem(y, ely)
            g.purge()
            continue
        steps[depth] = (x, y)
        seen.add(g)
        if g.win():
            return True
        if not dfs(g, steps, seen, depth+1):
            g.add_elem(x, elx)
            g.add_elem(y, ely)
            g.purge()
        else:
            return True
    return False


if __name__ == "__main__":
    g = np.load('test.npy').item()
    #  visual.draw_grid(g)
    print('start')
    print(solve(g))
