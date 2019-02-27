# Lamp 2

Project to control your raspberry-pi-zero-w unicornhathd lamp with your android phone.
This is the raspberry part.


# Requirements

You should have a raspberry pi zero w with header and a (fresh) install of [Raspian stretch light](https://www.raspberrypi.org/downloads/raspbian/) (Version: November 2018).

A [UNICORN HAT HD](https://shop.pimoroni.com/products/unicorn-hat-hd)

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

Note: If you want to see what your pi is doing, you can always open a (second) terminal to ssh to your pi (again). Then execute the command "htop" to watch your pi working.

## Step 3)
clone this repository to ~/ (thereby creating ~/lamp2 on your pi)

## Step 4)

execute "sudo raspi-config nonint do_spi 0"
then reboot your pi

use ssh (or the terminal on the pi) to navigate to ~/lamp2 ("cd ~/lamp2")

execute "./install.sh" (or open install.sh and run the commands step by step).

Wait. This will download and install dependencies. It takes a while.

after everything installed: shutdown the pi

## Step 5

Put the unicornhathd on the pi and start the pi again.

The Bluetooth still needs some work, but the unicornhathd should now be working.

You can test that by changing the directory to ~/lamp2 and running the command "python3 light_functions.py".
If everything went well, the lamp will light up and switch between 3 light patterns.

# Step 6

Now we will fix the bluetooth.
Basically, we will do [this](https://raspberrypi.stackexchange.com/questions/41776/failed-to-connect-to-sdp-server-on-ffffff000000-no-such-file-or-directory) fix.

In the terminal, type
sudo nano /etc/systemd/system/dbus-org.bluez.service

Search for the line

ExecStart=/usr/lib/bluetooth/bluetoothd

and change it to

ExecStart=/usr/lib/bluetooth/bluetoothd --compat

Press Ctrl+o followed by enter to save the changes. Exit the editor with Ctrl+X

reboot

Now the Bluetooth should be working.
Test that by navigating to "~/lamp2" and execute the command "sudo -E python3 main.py"
If the output looks like:

b''
except 2
Waiting for connection

Or:

b''
Waiting for connection

Then everything went well. You can exit the program with Ctrl+C

# Step 7
You can skip this, but it will make everything look a lot smoother, so I do not recommend skipping this.

We will now compile the python code to have more efficent running binarys.
To do that, just run the command "python3 compile.py build_ext --inplace".
It will take about 10 minutes or so.

NOTE: If you want to edit the python code later on, you first have to delete the matching "\*.so" file.
Otherwise python will use the ".so" file for imports and not the ".py" file. So you might wonder why your editing is not doing anything.


# Step 8

Now we will work on the autostart of the script.

Use the command "crontab -e" to edit.
Add the lines:

SHELL=/bin/bash

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin

@reboot source ~/.bashrc && ~/lamp2/lamp_autostart.sh > /home/pi/reboot.out

at the bottom.

Important: crontab has to end with new line! So at least one empty line on the bottom is very important!


# used as base:
Tutorial for bluetooth communication between Android and Raspberry:

http://it-in-der-hosentasche.blogspot.com/2014/03/bluetooth-zwischen-raspberry-pi-und.html

## Useful repositorys
I copied a lot of the light effects from here and changed the scripts to meet my requirements:
https://github.com/pimoroni/unicorn-hat-hd/tree/master/examples
https://github.com/pimoroni/unicorn-hat

# For the icons:
https://creativecommons.org/licenses/by/3.0/

https://www.iconfinder.com/iconsets/6x16-free-application-icons
