#!/usr/bin/env bash

# Created by Yannick Feld February 2019

# kill process started by lamp_autostart
if [[ $(ps -ef | grep "[s]udo -E $(echo ~)/lamp2/main.py") ]]; then
    sudo kill $(ps -ef | grep "[s]udo -E $(echo ~)/lamp2/main.py" | tr -s ' ' | cut -d ' ' -f 2)
    echo "killed off"
else
  echo "nothing to kill"
fi
