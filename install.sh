#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y
sudo raspi-config nonint do_spi 0
sudo apt-get install python3-pip python3-dev python3-spidev -y
pip3 install unicornhathd
sudo apt-get install python3-numpy -y
sudo apt-get install bluez -y
pip3 install pybluez
