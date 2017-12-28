#!/usr/bin/env python

import math
import os
import sys
import cv2

import hexgrid
from elements import Elem
import visual

center = (940, 349.5)
vertex1 = (940, 312.2)
vertex2 = (940, 273.8)

lw = math.sqrt((vertex1[0] - vertex2[0])**2 + (vertex1[1] - vertex2[1])**2)
lw_int = round(lw)
scale = lw * math.sqrt(3)
factor = 2.4

def get_hist(fp):
    img = cv2.imread(fp)
    h1 = cv2.calcHist([img], [0], None, [256], [0, 256])
    h2 = cv2.calcHist([img], [1], None, [256], [0, 256])
    h3 = cv2.calcHist([img], [2], None, [256], [0, 256])
    return (h1, h2, h3)

def get_histi(img):
    h1 = cv2.calcHist([img], [0], None, [256], [0, 256])
    h2 = cv2.calcHist([img], [1], None, [256], [0, 256])
    h3 = cv2.calcHist([img], [2], None, [256], [0, 256])
    return (h1, h2, h3)

def get_similar(hist1, hist2):
    i1 = cv2.compareHist(hist1[0], hist2[0], cv2.HISTCMP_CORREL)
    i2 = cv2.compareHist(hist1[1], hist2[1], cv2.HISTCMP_CORREL)
    i3 = cv2.compareHist(hist1[2], hist2[2], cv2.HISTCMP_CORREL)
    return (i1 + i2 + i3) / 3.

samples = {}
def init_sample():
    for el in Elem:
        fp = os.path.join('samples', el.name + '.png')
        fpi = os.path.join('samples', el.name + '-inactive.png')
        samples[el] = (get_hist(fp), get_hist(fpi))
    samples['empty'] = get_hist('samples/empty.png')
init_sample()


def get_img_at_pos(arr, coord):
    pcx, pcy = hexgrid.cartesian(coord, scale=scale)
    pcx, pcy = round(pcx + center[0]), round(center[1] - pcy)
    sub_img = arr[pcy-round(lw/factor):pcy+round(lw/factor)+1,
                  pcx-round(lw/factor):pcx+round(lw/factor)+1, :]
    return sub_img

def init_grid(fp):
    img = cv2.imread(fp)
    grid = hexgrid.HexGrid(6)
    for coord in grid.elements:
        sub_img = get_img_at_pos(img, coord)
        hist = get_histi(sub_img)
        max_si = get_similar(samples['empty'], hist)
        this_el = None
        active = False
        for el in Elem:
            s1 = get_similar(samples[el][0], hist)
            s2 = get_similar(samples[el][1], hist)
            if s1 > max_si:
                max_si = s1
                this_el = el
                active = True
            if s2 > max_si:
                max_si = s1
                this_el = el
                active = False
        if max_si > 0.4:
            grid.add_elem(coord, this_el)
            if active:
                grid.mk_active(coord)
        else:
            print(coord, max_si, this_el, active)
    return grid

if __name__ == "__main__":
    grid = init_grid('./luA3fgVy0HBZm9tAt1O4I82kgivo5NgH.png')
    visual.draw_grid(grid)
