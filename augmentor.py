#!/usr/bin/env python

import Augmentor

p = Augmentor.Pipeline("samples")
p.skew(0.5)
p.rotate(0.5, 10, 10)
p.random_distortion(0.7, 2, 2, 1)
p.shear(0.4, 8, 8)
p.zoom(0.5, 1.05, 1.1)
p.resize(1, 32, 32)
