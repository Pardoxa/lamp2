#!/usr/bin/env python3

# credit: https://raw.githubusercontent.com/pimoroni/unicorn-hat/master/examples/rainbow_blinky.py
import colorsys
import time
import random

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

def main(run, running):
    print("called")
    running(True)
    while run():
        x0, y0 = random.uniform(3.5,12.5), random.uniform(3.5,12.5)
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
            if t < 0.1:
                time.sleep(0.1 - t)
    unicorn.off()
    running(False)
