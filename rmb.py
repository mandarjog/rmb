import serial
import time
import rmb_cfg
import struct
import inspect

"""
pi@raspberrypi ~/roomba $ python
Python 2.7.3rc2 (default, May  6 2012, 20:02:25)
[GCC 4.6.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import rmb; rm = rmb.Roomba("/dev/ttyUSB0");
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
>>> rm.motors(1)
motors ['\x8a', '\x01']
>>> rm.motors(0)
motors ['\x8a', '\x00']
>>> rm.motors(2)
motors ['\x8a', '\x02']
>>> rm.motors(0)
motors ['\x8a', '\x00']
>>> rm.motors(4)
motors ['\x8a', '\x04']
>>> rm.motors(0)
motors ['\x8a', '\x00']
"""


def u16(num):
    """
    convert a number to 16 bit big endian representation
    """
    return struct.pack(">h", num) if num != 32768 else "\x80\x00"


class Roomba(object):

    """
    Basic SCI abstraction
    """

    def __init__(
        self,
        dev,
        baudrate=115200,
        timeout=0.1,
        delay=0.5,
            verbose=True):
        self.ser = serial.Serial(dev, baudrate=baudrate, timeout=timeout)
        self.delay = delay
        self.verbose = verbose
        self.start()
        self.full()

    def _cmd_(self, cmd, x=None):
        """
        execute command with optional arg
        """
        lcmd = [chr(rmb_cfg.OPCODE[cmd])]
        if x is not None:
            if isinstance(x, (int, long)):
                lcmd += chr(x)
            else:
                lcmd.extend(x)
        if self.verbose is True:
            print cmd, lcmd
        self.ser.write(lcmd)
        time.sleep(self.delay)
        return self.ser.readall()

    def __getattr__(self, cmd):
        if cmd in rmb_cfg.OPCODE:
            def icmd(x=None):
                return self._cmd_(cmd, x=x)
            setattr(self, cmd, icmd)
            return icmd
        else:
            raise AttributeError()

    def drive(self, velocity, radius):
        return self._cmd_("drive", u16(velocity) + u16(radius))

    def drive_stop(self):
        return self.drive(0, 0)

    def drive_straight(self, velocity):
        return self.drive(velocity, rmb_cfg.RADIUS["straight"])

    def sensors(self, packet_code=3):
        ds = self._cmd_("sensors", packet_code)
        sc = rmb_cfg.SCONFIG[packet_code]
        return sc["class"](*struct.unpack(sc["fmt"], ds))

    def song(self, num, notes, octave_bias=0, default_duration=64):
        outnotes = song(notes, octave_bias, default_duration)
        # enforce max length
        if len(outnotes) > 32:
            outnotes = outnotes[:32]
            print "Song truncated"
        self._cmd_("song", [chr(num), chr(len(outnotes) / 2)] + outnotes)

    def exec_script(self, cmds, pause_time=1.0):
        for cmd in cmds:
            spl = cmd.split(",")
            try:
                fn = getattr(self, spl[0])
                print "exec: ", cmd
                if len(spl) > 1:
                    ag = inspect.getargs(fn.func_code)
                    if len(ag.args) > 1:
                        ret = fn(*[int(i) for i in spl[1:]])
                    else:
                        ret = fn([chr(int(i)) for i in spl[1:]])
                else:
                    ret = fn()
                if ret:
                    print ret
                time.sleep(pause_time)
            except AttributeError:
                print "Cound not execute", cmd


def song(notes, octave_bias=0, default_duration=64):
    """
    C,C,0.5,+C,+C,1.2
    """
    if isinstance(notes, str):
        notes = notes.split(",")

    octavelen = len(rmb_cfg.NOTES)

    outnotes = []
    for note in notes:
        if len(outnotes) % 2 == 1:
            # we need to duration
            try:
                duration = float(note)
                duration = int(duration * default_duration)
                outnotes.append(chr(duration))
                continue
            except ValueError:
                outnotes.append(chr(default_duration))
        octave = 0
        if note.startswith('+'):
            octave = note.count('+')
        elif note.startswith('-'):
            octave = -1 * note.count('-')
        note = note[abs(octave):].lower()
        octave += octave_bias
        basenote_num = rmb_cfg.NOTES[note]
        note_num = basenote_num + octavelen * octave
        outnotes.append(chr(note_num))

    if len(outnotes) % 2 == 1:
        outnotes.append(chr(default_duration))

    return outnotes
