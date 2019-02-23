#!/usr/bin/env python3
import time

import icon_show
import subprocess
import ble2
import lightHandler
import unicornhathd as unicorn


def callback_print(var):
    print("Callbackprint %s", var)

if __name__ == '__main__':
    lightHandler.fill_unicorn(0,255,0)
    time.sleep(0.4)
    unicorn.off()
    startBluetoothCmd = "sudo systemctl start bluetooth"
    try:
        process = subprocess.Popen(startBluetoothCmd.split(), stdout = subprocess.PIPE)
        output, error = process.communicate()
    except:
        print("except 2")

    test = lightHandler.lightHandler()


    ble2.main(test.callback)
