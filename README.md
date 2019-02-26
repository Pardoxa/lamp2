# Lamp 2

Project to control your raspberry-pi-zero-w unicornhathd lamp with your android phone.
This is the raspberry part.


I plan to make clear/detailed instructions on how to run this code on your own Raspberry pi in the near future.

# Requirements

You should have a raspberry pi zero w with a (fresh) install of [Raspian stretch light](https://www.raspberrypi.org/downloads/raspbian/) (Version: November 2018).
A UNICORN HAT HD

# installation

## Step 1)
First, you should use raspi-config and change your password, default passwords are bad!
Then use the network options of raspi-config to connect to your WiFi.
reboot

## Step 2)
You can skip this step, if you want to work on the pi directly.

I prefere to use ssh for accessing the pi and sshfs to edit files on the pi.

If you want to change the hostname of the raspberry, use raspi-config to do so now.
Then/else stay in/ use raspi-config navigate to Interface options and turn on ssh.

reboot
You can now use "ssh pi@hostname" to access the pi.

To access the storage of your pi, use sshfs, see [this](https://www.raspberrypi.org/documentation/remote-access/ssh/sshfs.md) for more details
(Note: you can exchange the ip for the hostname of the pi).


## Step 3)
clone this repository to ~/ (thereby creating ~/lamp2 on your pi)

## Step 4) - this will take a while
use ssh (or the terminal on the pi) to navigate to ~/lamp2

execute "./install.sh" (or open install.sh and run the commands step by step).

Wait. This will download and install dependencies. It takes quite a while.
Plan at least 2 hours for this, probably more.
If you think your pi froze - it most certainly didn't.
You can open a second terminal to ssh to your pi. Then execute the command "htop" to watch your pi working.


# helpful for installation:
 https://raspberrypi.stackexchange.com/questions/55530/pybluez-and-gattlib-error


# used as base:
Tutorial for bluetooth communication between Android and Raspberry:

http://it-in-der-hosentasche.blogspot.com/2014/03/bluetooth-zwischen-raspberry-pi-und.html

## Useful repositorys
I copied a lot of the light effects from here and changed the scripts to meet my requirements:
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
