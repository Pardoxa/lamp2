#!/usr/bin/env python3


# See: https://github.com/pimoroni/unicorn-hat/blob/master/examples/drop.py
# it was used as base and changed to my needs

import time
from random import randint

import unicornhathd as unicorn

uh_width,uh_height=unicorn.get_shape()

heights = []

def setup():

    global heights
    heights = []
    for b in range(0, (uh_width-2)):
        heights.append(0)
    unicorn.off()
    for b in range(0, uh_height):
        unicorn.set_pixel(0, b, 255, 255, 255)
    for b in range(0, uh_height):
        unicorn.set_pixel((uh_width-1), b, 255, 255, 255)
    for b in range(1, (uh_width-1)):
        unicorn.set_pixel(b, 0, 255, 255, 255)
    unicorn.show()


def drop_ball(run):

    ball_colour = [randint(100, 255), randint(100, 255), randint(100, 255)]
    ball_column = randint(0, (uh_width-3))

    while heights[ball_column] == (uh_height-1):
        ball_column = randint(0, (uh_width-3))
    height = heights[ball_column]
    ball_y = (uh_height-1)
    unicorn.set_pixel(ball_column + 1, ball_y, ball_colour[0], ball_colour[1], ball_colour[2])
    unicorn.show()
    dropcount = (uh_height-2) - height
    for y in range(0, dropcount):
        unicorn.set_pixel(ball_column + 1, ball_y, 0, 0, 0)
        ball_y -= 1
        unicorn.set_pixel(ball_column + 1, ball_y, ball_colour[0], ball_colour[1], ball_colour[2])
        unicorn.show()
        time.sleep(0.02)
        if not run():
            return False
    heights[ball_column] += 1
    return True

def main(run, running):
    running(True)
    setup()
    shouldRun = run()
    while shouldRun:
        for i in range(0, (uh_width-2)*(uh_height-1)):
            shouldRun = drop_ball(run)
            if not shouldRun:
                break
        time.sleep(1)
        setup()
    unicorn.off()
    running(False)
