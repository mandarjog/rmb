#!/usr/bin/env python
import sys
import rmb


def get_args():
    import argparse
    argp = argparse.ArgumentParser()
    argp.add_argument("cmds", nargs="*")
    argp.add_argument('--dev', default="/dev/ttyUSB0")
    argp.add_argument('--pause-time', default=2.2, type=float)
    argp.add_argument('--verbose', default=False, action="store_true")
    return argp


def main(argv):
    argp = get_args()
    args = argp.parse_args(argv)

    if len(args.cmds) == 0:
        argp.print_help()
        return -1

    rm = rmb.Roomba(args.dev, verbose=args.verbose)
    return rm.exec_script(args.cmds, pause_time=args.pause_time)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

"""
pi@raspberrypi ~/rmb $ ./rmb_main.py --verbose drive,20,200 sensors,3 sensors,1 drive_stop
start ['\x80']
full ['\x84']
exec:  drive,20,200
drive ['\x89', '\x00', '\x14', '\x00', '\xc8']
exec:  sensors,3
sensors ['\x8e', '\x03']
s3(charging_state=4, voltage=15335, current=-336, temperature=33, charge=1957, capacity=2696)
exec:  sensors,1
sensors ['\x8e', '\x01']
s1(bumps_wheeldrops=0, wall=0, cliff_left=0, cliff_front_left=0, cliff_front_right=0, cliff_right=0, virtual_wall=0, motor_overcurrents=0, dirt_detector_left=0, dirt_detector_right=0)
exec:  drive_stop
drive ['\x89', '\x00', '\x00', '\x00', '\x00']
"""

