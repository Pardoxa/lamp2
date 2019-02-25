#!/bin/bash

# Created by Yannick Feld February 2019

# Script for cronjob - autostart of lamp
# Logs output of main.py in lamp.log (if you can't find the log: search for it in your home directory)

#sudo hciconfig hci0 piscan
echo "Starting Lamp"
nohup sudo -E ./lamp2/main.py > lamp.log &
