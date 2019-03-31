from __future__ import print_function
import unicornhathd as unicorn
import icon_show
import time
import _thread
import shlex
import argparse
import light_functions
import demo
import subprocess
import candle
import stars
import rainbow
import game_of_life
import drop
import rainbow_dot
import cross
import unicorn_clock
# created by Yannick Feld February 2019

parser = argparse.ArgumentParser(description= "Parsing bluetooth command strings")
parser.add_argument('--command', type=int)
parser.add_argument('--picture', type=str)
parser.add_argument('--color', type=str)
parser.add_argument('--bright', type=float)
parser.add_argument('--dur', type=int)
parser.add_argument('--rot', type=int)
parser.add_argument('--freq', type=int)
parser.add_argument('--flavor', type=int, action='append')
rot_arr = [0,90,180,270]
args = None
unicorn.rotation(0)
u_width, u_height = unicorn.get_shape()
unicorn.brightness(1.0)

def fill_unicorn(red, green, blue):
    for x in range(16):
        for y in range(16):
            unicorn.set_pixel(x,y,red,green,blue)
    unicorn.show()

class lightHandler():
    """docstring for lightHandler."""
    running = False
    status = 1
    _timer = time.monotonic()
    command = "1"
    def set_timer(self, t_in_s):
        self._timer = t_in_s + time.monotonic()

    def timer_over(self):
        if self.status == 10:
            self.status = 0
            return False
        return time.monotonic() < self._timer

    def get_status(self):
        return self.status

    def setRunning(self, running):
        self.running = running

    def shouldRun(self):
        return self.status == 0

    def callback(self, var):
        string_var = "%s" % var
        string_var = string_var[2:-1]
        #print("test:", end="\t")
        print(string_var)
        if string_var.startswith("|<>#~"):
            self.command = string_var
        else:
            self.command += string_var

        if self.command.endswith("~#><|"):
            print("Command:")
            print(self.command)
            args = self.parseCommand()
            self.handleCommand(args)

    def handleCommand(self, args):
        print("handleCommand")
        try:

            print(args.command)
            self.status = 10
            while self.running:
                print("waiting")
                time.sleep(0.1)
            self.status = 0
            unicorn.rotation(rot_arr[args.rot])
            unicorn.brightness(args.bright)
            print("set timer")
            self.set_timer(args.dur)
            print("Execute command",end = "\t")
            print(args.command)
            if args.command == 0:
                print("inside 10 - color")
                list = args.color.split(",")
                print(list)
                _thread.start_new_thread(light_functions.Color, (list[0], list[1], list[2], self.timer_over, self.setRunning), )
            elif args.command == 20:
                _thread.start_new_thread(icon_show.icon_show, (self.timer_over, self.setRunning), )
            elif args.command == 30:
                _thread.start_new_thread(light_functions.setPicture, (args.picture, self.timer_over, self.setRunning), )
            elif args.command == 31:
                _thread.start_new_thread(light_functions.setPictureShow, (args.picture, self.timer_over, self.setRunning, args.freq), )
            elif args.command == 40:
                _thread.start_new_thread(demo.main, (self.timer_over, self.setRunning), )
            elif args.command == 41:
                _thread.start_new_thread(demo.run_swirl, (self.timer_over, self.setRunning), )
            elif args.command == 42:
                _thread.start_new_thread(demo.run_rainbow_search, (self.timer_over, self.setRunning), )
            elif args.command == 43:
                _thread.start_new_thread(demo.run_tunnel, (self.timer_over, self.setRunning), )
            elif args.command == 44:
                _thread.start_new_thread(demo.run_checker, (self.timer_over, self.setRunning), )
            elif args.command == 45:
                _thread.start_new_thread(demo.run_gradient, (self.timer_over, self.setRunning), )
            elif args.command == 50:
                list = args.color.split(",")
                print(list)
                unicorn.rotation(rot_arr[(args.rot + 1) % 4])
                _thread.start_new_thread(light_functions.eye, (self.timer_over, self.setRunning, list[0], list[1], list[2]), )
            elif args.command == -1:
                fill_unicorn(255,0,0);
                time.sleep(0.4)
                unicorn.off()
                time.sleep(0.1)
                fill_unicorn(0,255,0)
                time.sleep(0.4)
                unicorn.off()
                time.sleep(0.1)
                fill_unicorn(0,0,255)
                time.sleep(0.4)
                unicorn.off()
                cmd = "sudo shutdown -h now"
                process = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
                output, error = process.communicate()
            elif args.command == 60:
                unicorn.rotation(rot_arr[(args.rot - 1) % 4])
                _thread.start_new_thread(candle.main, (self.timer_over, self.setRunning), )
            elif args.command == 70:
                _thread.start_new_thread(stars.main, (self.timer_over, self.setRunning), )
            elif args.command == 80:
                _thread.start_new_thread(rainbow.main, (self.timer_over, self.setRunning), )
            elif args.command == 90:
                _thread.start_new_thread(game_of_life.main, (self.timer_over, self.setRunning), )
            elif args.command == 100:
                _thread.start_new_thread(drop.main, (self.timer_over, self.setRunning), )
            elif args.command == 110:
                print("rainbow_dot")
                _thread.start_new_thread(rainbow_dot.main, (self.timer_over, self.setRunning), )
            elif args.command == 120:
                _thread.start_new_thread(cross.main, (self.timer_over, self.setRunning), )
            elif args.command == 130:
                _thread.start_new_thread(unicorn_clock.main, (self.timer_over, self.setRunning), )
            elif args.command == 140:
                _thread.start_new_thread(light_functions.hsv_wave, (self.timer_over, self.setRunning, args.flavor), )

            # _thread.start_new_thread(dev.run, (), )
        except:
            print("ERROR")

    def parseCommand(self):
        try:
            command = self.command[6:-6]
            print(command)
            args = parser.parse_args(shlex.split(command))
            if args.flavor == None:
                args.flavor = [0,0,1,10]
            #print("Command", end= "\t")
            print(args.command)
            #print(args.picture)
            return args
        except:
            print("Handle Command error")
            return None

    def runIconShow(self):

        self.setRunning(True)
        icon_show.icon_show(self.timer_over)
        self.setRunning(False)
