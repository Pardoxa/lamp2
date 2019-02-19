from communication import Device
import callback
import time
import _thread
import lightshow

if __name__ == '__main__':
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
