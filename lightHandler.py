import unicornhathd as unicorn
import icon_show
import time
import _thread
import shlex
import argparse
import light_color
import heart

parser = argparse.ArgumentParser(description= "Parsing bluetooth command strings")
parser.add_argument('--command', type=int)
parser.add_argument('--picture', type=str)
parser.add_argument('--color', type=str)
parser.add_argument('--bright', type=float)
parser.add_argument('--dur', type=int)
args = None
unicorn.rotation(0)
u_width, u_height = unicorn.get_shape()
unicorn.brightness(1.0)

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
        print("test:", end="\t")
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

            print("set timer")
            print(args.command)
            self.set_timer(args.dur)
            unicorn.brightness(args.bright)
            self.status = 10
            while self.running:
                print("waiting")
                time.sleep(0.1)
            self.status = 0

            if args.command == 0:
                print("inside 10 - color")
                list = args.color.split(",")
                print(list)

                _thread.start_new_thread(light_color.setColor, (list[0], list[1], list[2], self.timer_over, self.setRunning), )
            elif args.command == 20:
                _thread.start_new_thread(icon_show.icon_show, (self.timer_over, self.setRunning), )
            elif args.command == 30:
                _thread.start_new_thread(light_color.setPicture, (args.picture, self.timer_over, self.setRunning), )
            elif args.command == 40:
                _thread.start_new_thread(heart.main, (self.timer_over, self.setRunning), )
            elif args.command == 41:
                _thread.start_new_thread(heart.run_swirl, (self.timer_over, self.setRunning), )
            elif args.command == 42:
                _thread.start_new_thread(heart.run_rainbow_search, (self.timer_over, self.setRunning), )
            elif args.command == 43:
                _thread.start_new_thread(heart.run_tunnel, (self.timer_over, self.setRunning), )
            elif args.command == 44:
                _thread.start_new_thread(heart.run_checker, (self.timer_over, self.setRunning), )
            elif args.command == 45:
                _thread.start_new_thread(heart.run_gradient, (self.timer_over, self.setRunning), )

            # _thread.start_new_thread(dev.run, (), )
        except:
            print("ERROR")

    def parseCommand(self):
        try:
            command = self.command[6:-6]
            print(command)
            args = parser.parse_args(shlex.split(command))
            print("Command", end= "\t")
            print(args.command)
            print(args.picture)
            return args
        except:
            print("Handle Command error")
            return None

    def runIconShow(self):

        self.setRunning(True)
        icon_show.icon_show(self.timer_over)
        self.setRunning(False)
