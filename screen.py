#!/usr/bin/env python

import math
import os
import sys
import cv2
import uuid


from keras.models import load_model
import numpy as np
from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


import hexgrid
from elements import Elem
import visual

model_file = 'model.h5'
model = load_model(model_file)

center = (940, 349.5)
vertex1 = (940, 312.2)
vertex2 = (940, 273.8)

lw = math.sqrt((vertex1[0] - vertex2[0])**2 + (vertex1[1] - vertex2[1])**2)
lw_int = round(lw)
scale = lw * math.sqrt(3)
#  factor = 2.4
factor = 2.4


def get_img_at_pos(arr, coord):
    pcx, pcy = hexgrid.cartesian(coord, scale=scale)
    pcx, pcy = round(pcx + center[0]), round(center[1] - pcy)
    sub_img = arr[pcy-round(lw/factor):pcy+round(lw/factor)+1,
                  pcx-round(lw/factor):pcx+round(lw/factor)+1, :]
    return sub_img[:32, :32, :]


def predict(img):
    labels = model.predict_classes(img)
    return labels_map[labels[0]]

def init_grid(img):
    grid = hexgrid.HexGrid(6)
    for coord in grid.elements:
        sub_img = get_img_at_pos(img, coord)
        label = model.predict_classes(sub_img)
        grid.add_elem(coord, labels_map[label[0]])
    grid.purge()
    return grid


def get_grid():
    #  img = cv2.imread('./wBdn5OZ6SfZaL9wCLq3Qk0ydXH7RqQgP.png')
    #  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = load_image('./wBdn5OZ6SfZaL9wCLq3Qk0ydXH7RqQgP.png')
    return init_grid(img)

def mk_data(fp):
    img = Image.open(fp)
    img = np.asarray(img.convert('RGB'))
    grid = hexgrid.HexGrid(6)
    for coord in grid.elements:
        rnd = str(uuid.uuid4())
        sub_img = get_img_at_pos(img, coord)
        Image.fromarray(sub_img).save(f'storage/{rnd}.png')

def load_image(im):
    if isinstance(im, str):
        img = Image.open(im)
        img = np.asarray(img.convert('RGB')) / 255.
    elif isinstance(im, np.ndarray):
        img = im
    elif callable(im):
        img = im()
    else:
        raise ValueError("must be image path or numpy's ndarray")
    return img

labels = sorted(os.listdir('samples'))
labels_map = {}
for i, name in enumerate(labels):
    if name != 'empty':
        labels_map[i] = eval(f'Elem.{name}')
    else:
        labels_map[i] = 'None'

import re
for i in os.listdir('.'):
    if re.findall('.png', i):
        print(i)
        mk_data(i)
#  if __name__ == "__main__":
    #  grid = get_grid()
    #  visual.draw_grid(grid)
    #  total = {}
    #  for el in Elem:
        #  total[el] = 0
    #  for coord, el in grid.elements.items():
        #  if el is not None:
            #  total[el] += 1
    #  for el in Elem:
        #  print(el, total[el])
#  labels = open('./data/label_list.txt', 'r').read().splitlines() + \
            #  ['none']
#  labels = np.array(labels)
