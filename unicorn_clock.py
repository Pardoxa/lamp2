#!/usr/bin/env python

import signal
import threading
import time

# https://github.com/pimoroni/unicorn-hat/blob/master/examples/hat/clock.py

from graphics import Drawing, Color
import unicornhathd as unicorn



class UnicornDrawing(Drawing):
  def __init__(self):
    Drawing.__init__(self,16,16)

  '''
  All drawing operations use the pixel method
  so we override it for UnicornHat
  '''
  def pixel(self, x, y, col):
    if x < 0 or x > 15 or y < 0 or y > 15:
      return False
    self.buffer[(x,y)] = col
    unicorn.set_pixel(x, y, col.r, col.g, col.b)

  def show(self):
    unicorn.show()

d = UnicornDrawing()

# X offset of clock centre
O_X = 8
# Y offset of clock centre
O_Y = 8
# Radius of clock
R = 6
# Rotation offset of clock, set to 0, 90, 180, 270, etc
unicorn.rotation(0)

def setBrightness(currenttime):
  currenthour = currenttime.tm_hour
  # if it's between 10 am and 8 pm,
  # use dimmer brightness
  if(currenthour < 10 or currenthour > 20):
    unicorn.brightness(0.5)
  else:
    unicorn.brightness(0.8)

def tick():
  currenttime = time.localtime()
  currenthour = currenttime.tm_hour
  currentmin  = currenttime.tm_min
  currentsec  = currenttime.tm_sec

  # Set daytime or nighttime brightness
  setBrightness(currenttime)

  d.clear()
  # Draw the circle around the clock
  d.circle(O_X,O_Y,R,Color(255,0,255))

  # Draw the clock hands
  d.circle_line(O_X,O_Y,R-1,(-360.0*((currenthour % 12)/12.0)),Color(255,0,0))
  d.circle_line(O_X,O_Y,R-1,(-360.0*(currentmin/60.0)), Color(0,255,0))
  d.circle_line(O_X,O_Y,R-1,(-360.0*(currentsec/60.0)), Color(0,0,255))

  # draw buffer to hardware
  d.show()



def main(run, running):
    running(True)
    while run():
        tick()
        now = time.monotonic()
        time.sleep(now %0.01)
    unicorn.off()
    running(False)

if __name__ == '__main__':
    main()