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


sift = cv2.xfeatures2d.SIFT_create(contrastThreshold=0.004)
def get_des(fp):
    img = cv2.imread(fp, 0)
    #  cv2.equalizeHist(img)
    _, des = sift.detectAndCompute(img, None)
    return des

def get_desi(img):
    #  cv2.equalizeHist(img)
    _, des = sift.detectAndCompute(img, None)
    return des

samples = {}
def init_sample():
    for el in Elem:
        fp = os.path.join('samples', el.name + '.png')
        fpi = os.path.join('samples', el.name + '-inactive.png')
        samples[el] = (get_des(fp), get_des(fpi))
init_sample()

def get_img_at_pos(arr, coord):
    pcx, pcy = hexgrid.cartesian(coord, scale=scale)
    pcx, pcy = round(pcx + center[0]), round(center[1] - pcy)
    sub_img = arr[pcy-round(lw/factor):pcy+round(lw/factor)+1,
                  pcx-round(lw/factor):pcx+round(lw/factor)+1]
    return sub_img


bf = cv2.BFMatcher()
def get_matches(des1, des2):
    nm = 0
    matches = bf.knnMatch(des1, des2, k=2)
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            nm += 1
    return nm


def init_grid(img):
    grid = hexgrid.HexGrid(6)
    for coord in grid.elements:
        sub_img = get_img_at_pos(img, coord)
        des = get_desi(sub_img)
        max_match = 0
        this_el = None
        for el in Elem:
            cand1 = get_matches(des, samples[el][0])
            cand2 = get_matches(des, samples[el][1])
            cand = max(cand1, cand2)
            if cand > max_match:
                max_match = cand
                this_el = el
        if max_match >= 3:
            grid.add_elem(coord, this_el)
        else:
            #  print(coord, max_match, this_el)
            pass
    grid.purge()
    return grid


def get_grid():
    img = cv2.imread('./luA3fgVy0HBZm9tAt1O4I82kgivo5NgH.png', 0)
    return init_grid(img)

if __name__ == "__main__":
    grid = get_grid()
    visual.draw_grid(grid)
    total = {}
    for el in Elem:
        total[el] = 0
    for coord, el in grid.elements.items():
        if el is not None:
            total[el] += 1
    for el in Elem:
        print(el, total[el])
