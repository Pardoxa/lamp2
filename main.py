from communication import Device
import callback

if __name__ == '__main__':
    from hcisocket_linux import HCISocket
    dev = Device().withSocket( HCISocket(devId=0) )
    
    dev.start()
