#!/usr/bin/env python3

# See: https://github.com/pimoroni/unicorn-hat-hd/blob/master/examples/stars.py
# Which was used as base and changed to fit my needs

import random
from random import randint
import unicornhathd

def main(run, running):
    running(True)

    star_count = randint(20,25)
    star_speed = 0.05
    stars = []

    for i in range(0, star_count):
        stars.append((random.uniform(4, 11), random.uniform(4, 11), 0))


    while run():
        unicornhathd.clear()

        for i in range(0, star_count):
            stars[i] = (
                stars[i][0] + ((stars[i][0] - 8.1) * star_speed),
                stars[i][1] + ((stars[i][1] - 8.1) * star_speed),
                stars[i][2] + star_speed * 50)

            if stars[i][0] < 0 or stars[i][1] < 0 or stars[i][0] > 16 or stars[i][1] > 16:
                stars[i] = (random.uniform(4, 11), random.uniform(4, 11), 0)

            v = stars[i][2]

            unicornhathd.set_pixel(stars[i][0], stars[i][1], v, v, v)

        unicornhathd.show()
    unicornhathd.off()
    running(False)
