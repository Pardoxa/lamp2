from __future__ import print_function
import unicornhathd as unicorn
import time
from PIL import Image
import numpy as np
from random import randint
from random import uniform
import subprocess
import math
import colorsys
from itertools import cycle
import re

# Created by Yannick Feld February 2019

"""
    Contains functions called by lightHandler:

    hsv_wave
    eye
    Color
    setPicture
"""

u_width, u_height = unicorn.get_shape()

dists = np.zeros((16,16))
v_map = np.zeros((16,16))

# creates map of distances from x0 and y0 for pixels, creates v_map (v from hsv) based on distance
def make_mapping(v, x0, y0, with_hue = True):
    global dists
    global v_map

    for x in range(16):
        for y in range(16):
            dists[x][y] = (x - x0) * (x - x0) + (y - y0) * (y - y0)
    np.sqrt(dists, out = dists)
    if with_hue:
        maximum = np.amax(dists)
        v_times_inverseMaximum = v / maximum
        v_map = (maximum - dists) * v_times_inverseMaximum


def hsv_wave(run, running):
    global dists
    running(True)

    v = 1

    # x0, y0 current center
    x0 = uniform(0,15)
    y0 = uniform(0,15)

    # y_goal, x_goal -> goal
    y_goal = uniform(0,15)
    x_goal = uniform(0,15)
    step1 = uniform(0, math.pi * 2)
    step2 = uniform(0, math.pi * 2)
    while run() and v != 0:
        if x0 == x_goal and y0 == y_goal:
            print("hsv_wave - arrived",end="\tx:\t")
            print(x_goal,end="\ty:\t")
            print(y_goal)

            # goal reached, create new goal
            y_goal = uniform(0,15)
            x_goal = uniform(0,15)

        direction = [x_goal - x0, y_goal - y0]
        distance = np.linalg.norm(direction)

        # 0.05 is max velocity of movement
        if distance > 0.05:
            rescale = 0.05 / distance
            direction[0] *= rescale
            direction[1] *= rescale

        # move towards goal
        x0 += direction[0]
        y0 += direction[1]

        # create dists and v_map
        make_mapping(v, x0, y0)
        maximum = np.amax(dists)
        dists *= math.pi / maximum

        # set colors
        for x in range(u_width):
            for y, v_from_v_map, mapped_distance in zip(range(u_height), v_map[x], dists[x]):
                h = (math.sin(step1 + mapped_distance) + 1) * 0.5
                s = math.sqrt((math.sin(step2 + mapped_distance) + 1) * 0.5)
                unicorn.set_pixel_hsv(x, y, h, s, v_from_v_map)

        step1 += math.pi * 0.01
        step2 += math.e * 0.01
        unicorn.show()

    unicorn.off()
    running(False)

def _constrain(x):
    if x < 0:
        x = 0
    elif x > 15:
        x = 15
    return x

def constrain(x, y):
    return _constrain(x), _constrain(y)

def Color(h, s, v, run, running):
    running(True)
    h = float(h) / 360.0
    s = float(s)
    v = float(v)
    # x0, y0 current center
    x0 = uniform(0,15)
    y0 = uniform(0,15)

    # y_goal, x_goal -> goal
    y_goal = uniform(0,15)
    x_goal = uniform(0,15)
    while run() and v != 0:
        if x0 == x_goal and y0 == y_goal:
            print("color - arrived",end="\tx:\t")
            print(x_goal,end="\ty:\t")
            print(y_goal)

            # goal reached, create new goal
            y_goal = uniform(0,15)
            x_goal = uniform(0,15)

        direction = [x_goal - x0, y_goal - y0]
        distance = np.linalg.norm(direction)

        # 0.05 is max velocity of movement
        if distance > 0.05:
            rescale = 0.05 / distance
            direction[0] *= rescale
            direction[1] *= rescale

        # move towards goal
        x0 += direction[0]
        y0 += direction[1]

        #create dists and v_map
        make_mapping(v,x0,y0)

        for x in range(u_width):
            for y, v_from_v_map in zip(range(u_height), v_map[x]):
                unicorn.set_pixel_hsv(x, y, h, s, v_from_v_map)
        unicorn.show()

    unicorn.off()
    running(False)

def setPicture(pic, run, running):
    running(True)
    pic = decompress(pic)
    list = re.findall('......', pic)
    x = 0
    y = 0
    for val in list:
        pixel = fromHex(val)
        unicorn.set_pixel(x, y, pixel[0], pixel[1], pixel[2])

        x += 1
        if x == 16:
            x = 0
            y += 1
    unicorn.show()
    while run():
        time.sleep(0.01)
    unicorn.off()
    running(False)

# https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
def fromHex(hex):
    hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2 ,4))

def decompress(compressed):
    temp = compressed.split("x")
    temp = [x for x in temp if x]
    depressed = str("")
    for i in range(len(temp)):
        if len(temp[i]) >= 6:
            depressed += str(temp[i])
        else:
            depressed += depressed[-6:] * int(temp[i])

    return depressed

def setPictureShow(pic, run, running, frequency):
    running(True)
    pictureList = pic.split("|")

    list_cycle = cycle(pictureList)
    continue_loop = run()
    while continue_loop:
        x = 0
        y = 0
        current_list = next(list_cycle)
        current_list = decompress(current_list)
        if(current_list == None or len(current_list) != 256 * 6):
            continue_loop = run()
            continue

        list = re.findall('......', current_list)
        for val in list:
            pixel = fromHex(val)
            unicorn.set_pixel(x,y, pixel[0], pixel[1], pixel[2])
            x += 1
            if x == 16:
                x = 0
                y += 1
        unicorn.show()
        now = time.monotonic()
        while time.monotonic() < now + frequency:
            continue_loop = run()
            if not continue_loop:
                break;
            else:
                time.sleep(0.05)
    unicorn.off()

    running(False)

circle = np.array([
            np.array([0,0,0,0,0.149019607843,0.545098039216,0.811764705882,0.945098039216,0.945098039216,0.827450980392,0.56862745098,0.164705882353,0,0,0,0]),
            np.array([0,0,0.0156862745098,0.537254901961,0.98431372549,1.0,1.0,1.0,1.0,1.0,1.0,0.992156862745,0.58431372549,0.0313725490196,0,0]),
            np.array([0,0.0156862745098,0.686274509804,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.733333333333,0.0313725490196,0]),
            np.array([0,0.529411764706,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.6,0]),
            np.array([0.141176470588,0.98431372549,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.992156862745,0.180392156863]),
            np.array([0.529411764706,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.592156862745]),
            np.array([0.780392156863,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.850980392157]),
            np.array([0.913725490196,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.960784313725]),
            np.array([0.913725490196,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.960784313725]),
            np.array([0.788235294118,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.850980392157]),
            np.array([0.529411764706,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.592156862745]),
            np.array([0.133333333333,0.98431372549,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.992156862745,0.188235294118]),
            np.array([0,0.537254901961,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.6,0]),
            np.array([0,0.0156862745098,0.686274509804,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.741176470588,0.0313725490196,0]),
            np.array([0,0,0.0156862745098,0.545098039216,0.98431372549,1.0,1.0,1.0,1.0,1.0,1.0,0.992156862745,0.592156862745,0.0313725490196,0,0]),
            np.array([0,0,0,0,0.149019607843,0.552941176471,0.811764705882,0.945098039216,0.952941176471,0.827450980392,0.56862745098,0.172549019608,0,0,0,0])
        ])
# rgb_picture, because hsv is slow and I can reuse the rgb values
rgb_picture = np.zeros((16,16,3),dtype = int)

def eye_helper(center_x, center_y, h, s, v, calc_dist = True):
    global dists
    global circle
    global rgb_picture
    if calc_dist:
        # calculate distances
        make_mapping(1, center_x, center_y, False)

        # map inverse distance to brightness
        maximum = np.amax(dists)
        dists = v * (maximum - dists) / maximum

        # mask with circle
        np.multiply(dists, circle, out = dists)

        # map hsv values to rgb_picture
        for x in range(16):
            for y in range(16):
                temp = colorsys.hsv_to_rgb(h, s, dists[x][y])
                for i in range(3):
                    rgb_picture[x][y][i] = int(temp[i] * 255)
        #print(rgb_picture)
    for x in range(16):
        for y, rgb in zip(range(16), rgb_picture[x]):

            unicorn.set_pixel(x, y, rgb[0], rgb[1], rgb[2])

    # draw iris
    for x in range(center_x - 1, center_x + 2):
        for y in range(center_y - 1, center_y + 2):
            unicorn.set_pixel(x, y, 0, 0, 0)
    for y in [center_y - 2, center_y + 2]:
        unicorn.set_pixel(center_x, y, 0, 0, 0)


def eye(run, running, h, s, v):
    h = float(h) / 360.0
    s = float(s)
    v = float(v)

    running(True)

    eye_helper(8, 8, h, s, v)

    unicorn.show()
    twice = False
    last_blinked = time.monotonic()

    # random iris position
    position_x = randint(5, 12)
    position_y = randint(5, 12)

    edges = [5, 12]

    # don't allow the outer edges
    while position_x in edges and position_y in edges:
        position_x = randint(5, 12)
        position_y = randint(5, 12)

    while run():
        if not twice:
            time.sleep(uniform(0.2, 0.5))
        blink = False

        # where is the eye looking
        if randint(0, 1000) > 800:
            position_x = randint(5, 12)
            position_y = randint(5, 12)

            # don't allow the outer edges
            while position_x in edges and position_y in edges:
                position_x = randint(5, 12)
                position_y = randint(5, 12)

            # draw eye
            eye_helper(position_x, position_y, h, s, v)
            unicorn.show()

        # should it blink? (twice?)
        if randint(0,1000) > 950 and not twice:
            blink = True
            twice = randint(0, 100) > 70

        # blink if random number says so or 5 seconds have passed since last blink
        if blink or twice or time.monotonic() - last_blinked > 5:

            if blink:
                blink = False
            elif twice:
                twice = False

            # close eye
            for y in range(8):
                for x in range (16):
                    unicorn.set_pixel(x, y, 0, 0, 0)
                    unicorn.set_pixel(x, 15 - y, 0, 0, 0)
                unicorn.show()
                time.sleep(0.003)

            # open eye
            for i in reversed(range(8)):
                eye_helper(position_x, position_y, h, s, v, calc_dist = False )
                for y in range(i):
                    for x in range (16):
                        unicorn.set_pixel(x, y, 0, 0, 0)
                        unicorn.set_pixel(x, 15 - y, 0, 0, 0)
                unicorn.show()

            if not twice:
                time.sleep(0.5)

            last_blinked = time.monotonic()

    unicorn.off()
    running(False)

class test_handler():
    seconds = None
    endTime = time.monotonic()
    """ For testing the lightfunctions without bluetooth """
    def __init__(self, seconds):
        self.seconds = seconds


    def test_run(self):
        return time.monotonic() < self.endTime

    def test_running(self, started):
        if started:
            self.endTime = time.monotonic() + self.seconds

def main():
    handler = test_handler(5)
    try:
        print("Press Ctrl+C to exit")
        unicorn.brightness(0.5)
        #setColor(255,0,255,test_run,test_running)
        while True:
            hsv_wave(handler.test_run, handler.test_running)
            eye(handler.test_run, handler.test_running, 0.5, 0.9, 1)
            Color(0.7, 0.9, 1, handler.test_run, handler.test_running)
    except KeyboardInterrupt:
        unicorn.off()

if __name__ == '__main__':
    main()
