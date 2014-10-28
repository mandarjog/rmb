import serial
import time
"""
pi@raspberrypi ~/roomba $ python
Python 2.7.3rc2 (default, May  6 2012, 20:02:25)
[GCC 4.6.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import rmb; rm = rmb.Roomba("/dev/ttyUSB0"); rm.cmd_start(); rm.cmd_full()
start ['\x80']
full ['\x84']
>>> rm.drive_straight(20)
drive ['\x89', '\x00', '\x14', '\x80', '\x00']
>>> rm.drive_stop()
drive ['\x89', '\x00', '\x00', '\x00', '\x00']
>>> rm.drive(20, 30)
drive ['\x89', '\x00', '\x14', '\x00', '\x1e']
>>> rm.drive_stop()
drive ['\x89', '\x00', '\x00', '\x00', '\x00']
>>> rm.cmd_motors(1)
motors ['\x8a', '\x01']
>>> rm.cmd_motors(0)
motors ['\x8a', '\x00']
>>> rm.cmd_motors(2)
motors ['\x8a', '\x02']
>>> rm.cmd_motors(0)
motors ['\x8a', '\x00']
>>> rm.cmd_motors(4)
motors ['\x8a', '\x04']
>>> rm.cmd_motors(0)
motors ['\x8a', '\x00']
"""

OPCODE = {
    "start": 128,
    "safe": 131,
    "full": 132,
    "power": 133,
    "spot": 134,
    "clean": 135,
    "max": 136,
    "drive": 137,
    "motors": 138,
    "leds": 139,
    "song": 140,
    "play": 141,
    "sensors": 142
}

RADIUS = {
    "turn":
    {"clockwise": -1,
     "counterclockwise": 1},
    "straight": 32768,
    "max": 2000
}


def u16(num):
    ss = hex(int(num) & 0xffff)[2:]
    ss = ("0" * (4 - len(ss))) + ss
    return [chr(int(x, 16)) for x in [ss[:2], ss[2:]]]


class Roomba(object):
    def __init__(self, dev, baudrate=115200, timeout=0.1):
        self.ser = serial.Serial(dev, baudrate=baudrate, timeout=timeout)

    def __getattr__(self, cmd):
        if cmd.startswith("cmd_") and cmd[4:] in OPCODE:
            def icmd(x=None):
                lcmd = [chr(OPCODE[cmd[4:]])]
                if x is not None:
                    if isinstance(x, (int, long)):
                        lcmd += chr(x)
                    else:
                        lcmd.extend(x)
                print cmd[4:], lcmd
                self.ser.write(lcmd)
                time.sleep(0.5)
            setattr(self, cmd, icmd)
            return icmd
        else:
            raise AttributeError()

    def drive(self, velocity, radius):
        self.cmd_drive(u16(velocity) + u16(radius))

    def drive_stop(self):
        self.drive(0, 0)

    def drive_straight(self, velocity):
        self.drive(velocity, RADIUS["straight"])
