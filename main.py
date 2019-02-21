
import time

import icon_show
import subprocess
import ble2
import lightHandler

def callback_print(var):
    print("Callbackprint %s", var)

if __name__ == '__main__':
    startBluetoothCmd = "sudo systemctl start bluetooth"
    try:
        process = subprocess.Popen(startBluetoothCmd.split(), stdout = subprocess.PIPE)
        output, error = process.communicate()
    except:
        print("except 2")

    test = lightHandler.lightHandler()


    ble2.main(test.callback)
