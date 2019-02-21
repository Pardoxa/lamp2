import unicornhathd as unicorn
import time

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
