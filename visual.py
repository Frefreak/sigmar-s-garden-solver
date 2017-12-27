#!/usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.collections import PatchCollection

import hexgrid
from elements import Elem


def tocolor(e):
    if isinstance(e, Elem):
        return e.color
    return 'white'


def draw_grid(grid):
    fig, ax = plt.subplots()
    ax.axis('equal')
    ax.axis('off')
    fig.tight_layout()
    radius = 0.57735  # 1 / math.sqrt(3)
    sz = grid.size
    ax.set_xlim([-1 * (sz + 0.5), sz + 0.5])
    ax.set_ylim([-1 * (sz + 0.5), sz + 0.5])

    polys = []
    for k, v in grid.elements.items():
        cart = hexgrid.cartesian(k)
        if k in grid.active:
            alpha = 1
        elif v is None:
            alpha = 1
        else:
            alpha = 0.5
        polys.append(RegularPolygon(cart, 6, radius, edgecolor="black",
                                    facecolor=tocolor(v), alpha=alpha))
        if isinstance(v, Elem):
            if k in grid.active:
                plt.text(*cart, v.name, va='center', ha='center', weight='bold')
            else:
                plt.text(*cart, v.name, va='center', ha='center', style='italic')
    collection = PatchCollection(polys, True)
    ax.add_collection(collection)

    plt.show()


if __name__ == "__main__":
    g = hexgrid.HexGrid(6)
    g.add_elem((5, 0), Elem.salt)
    for nb in hexgrid.neighbours((5, 0)):
        if g._in_grid(nb):
            g.add_elem(nb, Elem.fire)
    g.mk_active((4, 0))
    g.add_elem((0, 0), Elem.gold)
    g.add_elem((1, -1), Elem.water)
    g.add_elem((-1, 0), Elem.mors)
    g.add_elem((-1, 1), Elem.lead)
    g.add_elem((0, -1), Elem.air)
    g.add_elem((-1, -1), Elem.tin)
    g.add_elem((0, -2), Elem.quicksilver)
    g.add_elem((3, 0), Elem.vitae)
    g.purge()
    draw_grid(g)
