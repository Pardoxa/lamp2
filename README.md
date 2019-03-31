# Lamp 2

Project to control your raspberry-pi-zero-w unicornhathd lamp with your android phone.
This is the raspberry part.


# Requirements

You should have a raspberry pi zero w with header and a (fresh) install of [Raspian stretch light](https://www.raspberrypi.org/downloads/raspbian/) (Version: November 2018).

A [UNICORN HAT HD](https://shop.pimoroni.com/products/unicorn-hat-hd)

# installation

## Step 1
First, you should use `sudo raspi-config` and change your password, default passwords are bad!
Then use the network options of `raspi-config` to connect to your WiFi.

reboot the pi:
```bash
sudo reboot
```

## Step 2
You can skip this step, if you want to work on the pi directly.

I prefere to use `ssh` for accessing the pi and `sshfs` to edit files on the pi.

If you want to change the hostname of the raspberry, use `raspi-config` to do so now.
Then/else stay in/ use `sudo raspi-config` navigate to Interface options and turn on ssh.

reboot
You can now use `ssh pi@hostname` to access the pi.

To access the storage of your pi, use `sshfs`, see [this](https://www.raspberrypi.org/documentation/remote-access/ssh/sshfs.md) for more details
(Note: you can exchange the ip for the hostname of the pi).

Note: If you want to see what your pi is doing, you can always open a (second) terminal to ssh to your pi (again). Then execute the command `htop` to watch your pi working.

## Step 3

clone this repository:

```Bash
sudo apt-get update
sudo apt-get install git
cd
git clone https://github.com/Pardoxa/lamp2.git
```

It is important to clone the Repository to this specific location, since I hardcoded a few Paths.
I'm sorry for that, but this is just a freetime project and I only decided to make this repository public after I finished.

## Step 4

execute `sudo raspi-config nonint do_spi 0`
then reboot your pi

Now execute the commands:

```bash
cd ~/lamp2
./install.sh
```
(or look at install.sh and run the commands manually).

Wait. This will download and install dependencies. It takes a while.

after everything installed: shutdown the pi

```bash
sudo shutdown -h now
```

## Step 5

Put the unicornhathd on the pi and start the pi again.

The Bluetooth still needs some work, but the unicornhathd should now be working.

You can test that with:

```Bash
cd ~/lamp2
python3 light_functions.py
```

If everything went well, the lamp will light up and switch between 3 light patterns.

## Step 6

Now we will fix the bluetooth.
Basically, we will do [this](https://raspberrypi.stackexchange.com/questions/41776/failed-to-connect-to-sdp-server-on-ffffff000000-no-such-file-or-directory) fix.

In the terminal, type
```Bash
sudo nano /etc/systemd/system/dbus-org.bluez.service
```
Search for the line

`ExecStart=/usr/lib/bluetooth/bluetoothd`

and change it to

`ExecStart=/usr/lib/bluetooth/bluetoothd --compat`

Press Ctrl+o followed by enter to save the changes. Exit the editor with Ctrl+X

Then open the editor again, this time using:

```bash
sudo nano /etc/bluetooth/main.conf
```
and add the line:

```
DisablePlugins = pnat

```

I do not know if this file has to end with a newline, but it will not hurt if it does.

reboot

Now the Bluetooth should be working.
Test that with:
```Bash
cd ~/lamp2
sudo -E python3 main.py
```

If the output looks like:

```
b''
except 2
Waiting for connection
```

Or:

```
b''
Waiting for connection
```

Then everything went well. You can exit the program with Ctrl+C

## Step 7
You can skip this, but it will make everything look a lot smoother, so I do not recommend skipping this step.

We will now compile the python code to have more efficent running binarys.
To do that, just run the command:
```Bash
cd ~/lamp2
python3 compile.py build_ext --inplace
```
It will take about 10 minutes or so.

NOTE: If you want to edit the python code later on, you first have to delete the matching ".so" file.
Otherwise python will use the ".so" file for imports and not the ".py" file. So you might wonder why your editing is not doing anything.


## Step 8

Now we will work on the autostart of the script.

Use the command `crontab -e` to edit, add the lines:

```vim
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin
@reboot source ~/.bashrc && ~/lamp2/lamp_autostart.sh > /home/pi/reboot.out
```

You can change ` > /home/pi/reboot.out` to ` 2>&1> /dev/null` if you do not want logfiles from the autostart.

IMPORTANT: crontab has to end with new line! So at least one empty line on the bottom is very important!

To test if everything worked: reboot your pi.

After the pi bootet, the lamp should flash green.

## Step 9
Pair your android with your raspberry. You do not have to have the app installed yet.
To pair do the following:

kill the autostart script by running `~/lamp2/kill-autostart.sh`

then run `sudo hciconfig hci0 piscan`

Now turn on bluetooth on your android and search for your pi. You should see the pi (the name is the hostname of the pi).
Pair your phone with your android.

then reboot the pi.

Congratulations, you are done with the raspberry part. All that is left is installing the [app](https://github.com/Pardoxa/Lampe2) on your android.

Have fun :)

# Cancel Program started by autostart

If you want to cancel the script started by autostart, use:
```Bash
~/lamp2/kill-autostart.sh
```

Note: This will not turn off the UNICORN HAT HD. The Picture will just freeze.
If you want to turn off the light, just use the android app with the cancel command.
If for whatever reason you cannot and have killed the autostart script,
you can do it like this:

```bash
python3
```
```python
import unicornhathd as unicorn
unicorn.off()
```

If you want to manually start the scrip again, run:
```bash
~/lamp2/lamp_autostart.sh
```

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
