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


u_width, u_height = unicorn.get_shape()

dists = np.zeros((16,16))
hue_map = np.zeros((16,16))


def make_mapping(v, x0, y0, with_hue = True):
    global dists
    global hue_map

    for x in range(16):
        for y in range(16):
            dists[x][y] = (x - x0) * (x - x0) + (y - y0) * (y - y0)
    np.sqrt(dists, out = dists)
    if with_hue:
        maximum = np.amax(dists)
        v_times_inverseMaximum = v / maximum
        hue_map = (maximum - dists) * v_times_inverseMaximum


def hue_wave(run, running):
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
            print("hue_wave - arrived",end="\tx:\t")
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

        # create dists and hue_map
        make_mapping(v, x0, y0)
        maximum = np.amax(dists)
        dists *= math.pi / maximum

        # set colors
        for x in range(u_width):
            for y, v_from_hue_map, mapped_distance in zip(range(u_height), hue_map[x], dists[x]):
                h = (math.sin(step1 + mapped_distance) + 1) * 0.5
                s = (math.sin(step2 + mapped_distance) + 1) * 0.5
                unicorn.set_pixel_hsv(x, y, h, s, v_from_hue_map)

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

def setColor(h, s, v, run, running):
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

        #create dists and hue_map
        make_mapping(v,x0,y0)

        for x in range(u_width):
            for y, v_from_hue_map in zip(range(u_height), hue_map[x]):
                unicorn.set_pixel_hsv(x, y, h, s, v_from_hue_map)
        unicorn.show()

    unicorn.off()
    running(False)

def setPicture(pic, run, running):
    running(True)
    list = pic.split("#")
    x = 0
    y = 0
    for val in list:
        pixel = val.split(",")
        #print(int(pixel[0]), end = "\t")
    #    print(x, end = "\t")
    #    print(y)
        unicorn.set_pixel(x,y, int(pixel[0]), int(pixel[1]), int(pixel[2]))
        x += 1
        if x == 16:
            x = 0
            y += 1
    unicorn.show()
    while run():
        time.sleep(0.01)
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
            unicorn.set_pixel(x, y, 255, 255, 255)

    for x in [center_x - 2, center_x + 2]:
        for y in [center_y - 2, center_y + 2]:
            unicorn.set_pixel(x, y, 255, 255, 255)

def eye(run, running, h, s, v):
    global matrix
    h = float(h) / 360.0
    s = float(s)
    v = float(v)

    running(True)

    eye_helper(8, 8, h, s, v)

    unicorn.show()
    twice = False
    last_blinked = time.monotonic()

    # current eye position
    position_x = randint(5,12)
    position_y = randint(5,12)
    while run():
        if twice:
            time.sleep(uniform(0.05,0.2))
        else:
            time.sleep(uniform(0.1,0.5))
        blink = False
        if randint(0,1000) > 900:
            position_x = randint(5,12)
            position_y = randint(5,12)
            eye_helper(position_x, position_y, h, s, v)
        if randint(0,1000) > 950:
            blink = True
        if blink or twice or time.monotonic() - last_blinked > 5:
            last_blinked = time.monotonic()
            if twice:
                twice = False
            else:
                twice = randint(0,100) > 75

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
        unicorn.show()

    unicorn.off()
    print(matrix)
    running(False)

def test_run():
    return True

def test_running(var):
    pass

def main():
    unicorn.brightness(1)
    #setColor(255,0,255,test_run,test_running)
    hue_wave(test_run, test_running)

if __name__ == '__main__':
    main()
