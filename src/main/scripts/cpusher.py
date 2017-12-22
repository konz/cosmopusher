#!/usr/bin/env python

"""Cosmopusher. Reads and parses data from N560 pulse oxymeters and sends it to AWS SNS topics.

Usage:
  cpusher.py (-h | --help)
  cpusher.py (-d | --demo)

Options:
  -h --help     Show this screen.
  -d --demo     Send some demo data.
"""
import serial
from docopt import docopt
from gevent import monkey

from cosmopusher.demo_stream import DemoStream
from cosmopusher.n560reader import N560Reader
from cosmopusher.print_pusher import PrintPusher

if __name__ == '__main__':
    monkey.patch_all()

    arguments = docopt(__doc__)

    if arguments['--demo']:
        stream = DemoStream()
    else:
        stream = serial.Serial("/dev/serial0", timeout=10)

    reader = N560Reader(stream, PrintPusher)
    try:
        reader.run()
    except KeyboardInterrupt:
        print("exiting")
