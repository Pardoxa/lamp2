from communication import Device
import callback
import time

if __name__ == '__main__':
    from hcisocket_linux import HCISocket
    dev = Device().withSocket( HCISocket(devId=0) )

    status = dev.start()
    print(status.get_status())
    time.sleep(5)
    dev.run()
