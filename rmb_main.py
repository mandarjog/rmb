#!/usr/bin/env python
import sys
import rmb


def get_args():
    import argparse
    argp = argparse.ArgumentParser()
    argp.add_argument("cmds", nargs="*")
    argp.add_argument('--dev', default="/dev/ttyUSB0")
    argp.add_argument('--verbose', default=False, action="store_true")
    return argp


def main(argv):
    argp = get_args()
    args = argp.parse_args(argv)

    if len(args.cmds) == 0:
        argp.print_help()
        return -1

    rm = rmb.Roomba(args.dev, verbose=args.verbose)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
