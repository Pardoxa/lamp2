# Lamp 2

Project to control your raspberry-pi-zero-w unicornhathd lamp with your android phone.
This is the raspberry part.


I plan to make clear/detailed instructions on how to run this code on your own Raspberry pi in the near future.

# Requirements

You should have a raspberry pi zero w with a (fresh) install of [Raspian stretch light](https://www.raspberrypi.org/downloads/raspbian/) (Version: November 2018).

# helpful for installation:
 https://raspberrypi.stackexchange.com/questions/55530/pybluez-and-gattlib-error


# used as base:
Tutorial for bluetooth communication between Android and Raspberry:

http://it-in-der-hosentasche.blogspot.com/2014/03/bluetooth-zwischen-raspberry-pi-und.html

## Useful repositorys:
https://github.com/pimoroni/unicorn-hat-hd/tree/master/examples
https://github.com/pimoroni/unicorn-hat

# Fix
https://raspberrypi.stackexchange.com/questions/41776/failed-to-connect-to-sdp-server-on-ffffff000000-no-such-file-or-directory

# crontab:

to edit use: "crontab -e"
and add :

SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games


@reboot source ~/.bashrc && bash /home/pi/lamp2/lamp_autostart.sh > /home/pi/reboot.out


At the end of the crontab. Note: crontab has to end with new line!

Not everything in the Crontab is needed - filter not needed parts when I build the next lamp


# compile
python3 compile.py build_ext --inplace

# For the icons:
https://creativecommons.org/licenses/by/3.0/

https://www.iconfinder.com/iconsets/6x16-free-application-icons
