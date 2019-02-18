import time
import uuid


class Attribute:
    def __init__(self, att_type, value=None):
        self.handle = None
        self.typeUUID = uuid.UUID(att_type)
        self.value = value

    def setHandle(self, hnd):
        self.handle = hnd

    def getValue(self):
        return self.value

    def isWriteable(self):
        return False

    def setValue(self, value):
        raise CommandError(E_WRITE_NOT_PERMITTED, "Write not permitted", self.handle)

    def __str__(self):
        v = self.getValue()
        valstr = "<unset>" if (v is None) else binascii.b2a_hex(v).decode("ascii")
        return ("Attr hnd=0x%04X UUID=%s val=%s" % (self.handle, self.typeUUID.getCommonName(),
                   valstr ) )

class state(Attribute):
    """docstring for state."""
    status = 1
    _timer = time.monotonic()

    def __init__(self, charUUID, value=None):
        Attribute.__init__(self, charUUID, value)

    def setValue(self, value):
        self.value = value

    def isWriteable(self):
        return True

    def get(self):
        return self

    def set_timer(self, t_in_s):
        self._timer = t_in_s + time.monotonic()


    def timer_over(self):

        return time.monotonic() < self._timer

    def get_status(self):
        return self.status


def doSomething(_state):
    tmp = _state()
    bla = True
    while tmp.timer_over():
        if tmp.get_status:
            print(tmp._timer - time.monotonic())
            if bla and tmp._timer - time.monotonic() < 5:
                _state().set_timer(10)
                bla = False


def main():
    _state = state()
    _state.set_timer(10)
    doSomething(_state.get)


if __name__ == '__main__':
    main()
