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
#temp = np.zeros((16,16))
dists = np.zeros((16,16))
hue_map = np.zeros((16,16))

def make_mapping(v,x0,y0):
    global dists
    global hue_map
    #distances = [math.sqrt(int(i / 16) * int(i / 16) + int(i % 16)* int(i % 16)) for i in range(256)]
    for x in range(16):
        for y in range(16):
            dists[x][y] = (x - x0) * (x - x0) + (y - y0) * (y - y0)
    np.sqrt(dists, out = dists)
    maximum = np.amax(dists)
    v_times_inverseMaximum = v / maximum
    hue_map = (maximum - dists) * v_times_inverseMaximum
    #for x in range(16):
    #    for y in range(16):
    #        hue_map[x][y] = (maximum - dists[x][y]) * v_times_inverseMaximum


#def getPixel(x,y,x_offset,y_offset, map):
#    print(map)
#    return map[int(abs(x-x_offset))][int(abs(y-y_offset))]

def _constrain(x):
    if x < 0:
        x = 0
    elif x > 15:
        x = 15
    return x

def constrain(x, y):
    return _constrain(x), _constrain(y)

def setColor(red, green, blue, run, running):
    running(True)
    red = int(red)
    green = int(green)
    blue = int(blue)
    h,s,v = colorsys.rgb_to_hsv(red, green, blue)
    v /= 255
    x0 = 0
    y0 = 0
    y_goal = uniform(0,15)
    x_goal = uniform(0,15)
    while run() and v != 0:
        if x0 == x_goal and y0 == y_goal:
            print("angekommen",end="\tx:\t")
            print(x_goal,end="\ty:\t")
            print(y_goal)
            y_goal = uniform(0,15)
            x_goal = uniform(0,15)

        direction = [x_goal - x0, y_goal - y0]
        distance = np.linalg.norm(direction)
        #distance = math.sqrt(direction[0] * direction[0] + direction[1] * direction[1])
        if distance > 0.05:
            rescale = 0.05 / distance
            direction[0] *= rescale
            direction[1] *= rescale

        x0 += direction[0]
        y0 += direction[1]
        make_mapping(v,x0,y0)

        for x in range(u_width):
            for y, v_from_hue_map in zip(range(u_height), hue_map[x]):
                unicorn.set_pixel_hsv(x, y, h, s, v_from_hue_map)
                #unicorn.set_pixel_hsv(x,y,h,s,hue_map[x][y])
                #unicorn.set_pixel(x,y,red,green,blue)
        unicorn.show()
        #time.sleep(0.1)
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

def eye_helper(matrix, center_x, center_y):
    for x in range(16):
        for y in range(16):
            unicorn.set_pixel(x, y, matrix[x][y][0], matrix[x][y][1], matrix[x][y][2])
    for x in range(center_x-1,center_x+2):
        for y in range(center_y-1,center_y+2):
            unicorn.set_pixel(x,y,255,255,255)
    for x in [center_x-2, center_x+2]:
        for y in [center_y-2, center_y+2]:
            unicorn.set_pixel(x,y,255,255,255)
def eye(run, running, red, green, blue):
    running(True)
    cmd = "echo ~/lamp2/res/circle-16.png"
    process = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
    output, error = process.communicate()
    output = str(output)[2:-3]
    img = Image.open(output)
    img.load()
    try:
        background = Image.new("RGB", img.size, (0, 0, 0))
        background.paste(img, mask=img.split()[3]) # 3 is the alpha channel
    except:
        background = img
    A = np.asarray(background)
    matrix = [[[(int(var[0]) * int(i)) / 255 for i in [red, green, blue]] for var in list ] for list in A]


    eye_helper(matrix,8,8)

    unicorn.show()
    twice = False
    last_blinked = time.monotonic()
    while run():
        if twice:
            time.sleep(uniform(0.05,0.2))
        else:
            time.sleep(uniform(0.1,0.5))
        blink = False
        position_x = randint(5,12)
        position_y = randint(5,12)
        if randint(0,1000) > 900:
            eye_helper(matrix,position_x,position_y)
        if randint(0,1000) > 950:
            blink = True
        if blink or twice or time.monotonic() - last_blinked > 5:
            last_blinked = time.monotonic()
            if twice:
                twice = False
            else:
                twice = randint(0,100) > 75
            for y in range(8):
                for x in range (16):
                    unicorn.set_pixel(x,y,0,0,0)
                    unicorn.set_pixel(x,15-y,0,0,0)
                unicorn.show()
                time.sleep(0.003)
            for i in reversed(range(8)):
                eye_helper(matrix,position_x,position_y)
                for y in range(i):
                    for x in range (16):
                        unicorn.set_pixel(x,y,0,0,0)
                        unicorn.set_pixel(x,15-y,0,0,0)
                unicorn.show()
                time.sleep(0.001)
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
    setColor(255,0,255,test_run,test_running)
    #h,s, map = get_mapping(255,0,0)
    #for x in range(16):
    #    for y in range(16):
    #        print(map[x+y*16],end ="\t")
    #        unicorn.set_pixel_hsv(x,y,h,s,getPixel(x,y,3,0,map))
    #    print()
    #unicorn.show()

if __name__ == '__main__':
    main()
