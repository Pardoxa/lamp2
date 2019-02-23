# Lamp 2

The python project

# helpful for installation:
 https://raspberrypi.stackexchange.com/questions/55530/pybluez-and-gattlib-error


# used as base:

http://it-in-der-hosentasche.blogspot.com/2014/03/bluetooth-zwischen-raspberry-pi-und.html

## lamp:
https://github.com/pimoroni/unicorn-hat-hd/tree/master/examples

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
