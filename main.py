#!/usr/bin/env python3
import time

import icon_show
import subprocess
import bluetooth_to_android
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
        print(output)
        print("error:" + error)
    except:
        print("except 2")

    lamp_handler = lightHandler.lightHandler()

    bluetooth_to_android.main(lamp_handler.callback)
