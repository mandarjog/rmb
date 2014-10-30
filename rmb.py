import serial
import time
import rmb_cfg
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


def u16(num):
    """
    convert a number to 16 bit big endian representation
    """
    ss = hex(int(num) & 0xffff)[2:]
    ss = ("0" * (4 - len(ss))) + ss
    return [chr(int(x, 16)) for x in [ss[:2], ss[2:]]]


class Roomba(object):
    def __init__(self, dev, baudrate=115200, timeout=0.1, delay=0.5, verbose=True):
        self.ser = serial.Serial(dev, baudrate=baudrate, timeout=timeout)
        self.delay = delay
        self.verbose = verbose
        self.ser.cmd_start()
        self.ser.cmd_full()

    def __getattr__(self, cmd):
        if cmd.startswith("cmd_") and cmd[4:] in rmb_cfg.OPCODE:
            def icmd(x=None):
                lcmd = [chr(rmb_cfg.OPCODE[cmd[4:]])]
                if x is not None:
                    if isinstance(x, (int, long)):
                        lcmd += chr(x)
                    else:
                        lcmd.extend(x)
                if self.verbose is True:
                    print cmd[4:], lcmd
                self.ser.write(lcmd)
                time.sleep(self.delay)
            setattr(self, cmd, icmd)
            return icmd
        else:
            raise AttributeError()

    def drive(self, velocity, radius):
        self.cmd_drive(u16(velocity) + u16(radius))

    def drive_stop(self):
        self.drive(0, 0)

    def drive_straight(self, velocity):
        self.drive(velocity, rmb_cfg.RADIUS["straight"])
