import unicornhathd as unicorn
import time
from PIL import Image
import numpy as np
from random import randint
from random import uniform

u_width, u_height = unicorn.get_shape()

def setColor(red, green, blue, run, running):
    running(True)
    for x in range(u_width):
        for y in range(u_height):
            unicorn.set_pixel(x,y,red,green,blue)
    unicorn.show()
    while(run()):
        time.sleep(0.01)
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
    img = Image.open("./res/circle-16.png")
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
