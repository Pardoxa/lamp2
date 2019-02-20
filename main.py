
import callback
import time
import _thread
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

    try:
        _thread.start_new_thread(test.outerLoop, (), )
        # _thread.start_new_thread(dev.run, (), )
    except:
        print("ERROR")

    ble2.main(test.callback)
