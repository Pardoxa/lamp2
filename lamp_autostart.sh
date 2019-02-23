#!/bin/bash

echo "HELLO WORLD"
sudo -E echo "SUDO ECHO"
nohup sudo -E ./lamp2/main.py &
echo "after sudo echo"
echo $(pwd)
