#!/usr/bin/env python3

# See: https://raw.githubusercontent.com/pimoroni/unicorn-hat/master/examples/rainbow_blinky.py
# or: https://github.com/pimoroni/unicorn-hat/blob/master/examples/rainbow_blinky.py
# Which was used as base and changed to fit my needs

import colorsys
import time
import random
import math
import numpy

import unicornhathd as unicorn


width,height=unicorn.get_shape()

if height==width:
    delta=0
else:
    delta=2


def make_gaussian(fwhm,x0,y0):
    x = numpy.arange(0, 16, 1, float)
    y = x[:, numpy.newaxis]

    fwhm = fwhm
    gauss = numpy.exp(-4 * numpy.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
    return gauss

def constrain(var, lower, upper):
    if var < lower:
        return lower
    if var > upper:
        return upper
    return var

def main(run, running):
    print("called")
    running(True)
    x0 = 7.5
    y0 = 7.5
    while run():
        unicorn.off()
        time.sleep(0.03)
        angle = random.uniform(0, math.pi * 2)
        x0 += math.sin(angle)
        y0 += math.cos(angle)
        x0 = constrain(x0, 3.5, 12.5)
        y0 = constrain(y0, 3.5, 12.5)
        for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
            fwhm = 5.0/z
            gauss = make_gaussian(fwhm, x0,y0)
            start = time.time()
            for y in range(height):
                for x in range(width):
                    h = 1.0/(x + y + delta + 1)
                    s = 0.8
                    if height<=width:
                        v = gauss[x,y+delta]
                    else:
                        v = gauss[x+delta,y]
                    rgb = colorsys.hsv_to_rgb(h, s, v)
                    r = int(rgb[0]*255.0)
                    g = int(rgb[1]*255.0)
                    b = int(rgb[2]*255.0)
                    unicorn.set_pixel(x, y, r, g, b)
            unicorn.show()
            end = time.time()
            t = end - start
            if t < 0.11:
                time.sleep(0.11 - t)
    unicorn.off()
    running(False)
