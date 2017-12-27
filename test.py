#!/usr/bin/env python

import sys
import cv2
from skimage.measure import compare_ssim

img1 = cv2.imread(sys.argv[1])
img2 = cv2.imread(sys.argv[2])
#  img2.resize(img1.shape)
print(img1.shape)
print(img2.shape)
#  print(ssim(img1, img2))
