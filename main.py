from communication import Device
import callback
import time
import _thread
import lightshow
import subprocess

if __name__ == '__main__':
    startBluetoothCmd = "sudo systemctl start bluetooth"
    stopBluetoothCmd = "sudo systemctl stop bluetooth"
    try:
        process = subprocess.Popen(stopBluetoothCmd.split(), stdout = subprocess.PIPE)
        output, error = process.communicate()
    except:
        print("except 1")
    try:
        process = subprocess.Popen(startBluetoothCmd.split(), stdout = subprocess.PIPE)
        output, error = process.communicate()
    except:
        print("except 2")
    from hcisocket_linux import HCISocket
    dev = Device().withSocket( HCISocket(devId=0) )

    status = dev.start()
    print(status.get_status())
    light = lightshow.test_show(status)
    try:
        _thread.start_new_thread(light.blink, (), )
        # _thread.start_new_thread(dev.run, (), )
    except:
        print("ERROR")

    dev.run()
