#!/usr/bin/env python3

import colorsys
import math
import time
from itertools import cycle


import unicornhathd

unicornhathd.rotation(0)
u_width, u_height = unicornhathd.get_shape()
unicornhathd.brightness(1.0)
# Generate a lookup table for 8bit hue to RGB conversion
hue_to_rgb = []

for i in range(0, 255):
    hue_to_rgb.append(colorsys.hsv_to_rgb(i / 255.0, 1, 1))


class test_show:
    """docstring for test_show."""
    back = None
    def __init__(self, back):
        self.callback = back

    def blink(self):
        cr = cycle([0, 100, 200])
        cg = cycle([100, 1, 200, 90, 123, 124, 0])
        while self.callback.get_status() > 0:
            b = 0
            r = next(cr)
            g = next(cg)
            for y in range(u_height):
                for x in range(u_width):
                    unicornhathd.set_pixel(x, y, r, g, b)
            unicornhathd.show()
            time.sleep(3)
