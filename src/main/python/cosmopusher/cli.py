#!/usr/bin/env python

"""Cosmopusher. Reads and parses data from N560 pulse oxymeters and sends it to AWS IoT.

Usage:
  cpusher.py (-h | --help)
  cpusher.py (-d | --demo)
  cpusher.py [-d] --endpoint=ENDPOINT --root-ca=FILE [--topic=TOPIC_NAME]
  cpusher.py (-p | --print) [-d]

Options:
  -h --help                 Show this screen.
  -d --demo                 Send some demo data.
  -p --print                Instead of sending it to IoT, just print out the data.
                            (together with some simulation of delay)
  --endpoint=HOSTNAME       AWS IoT endpoint
  --root-ca=FILE            AWS IoT root certificate file
  --topic=TOPIC_NAME        AWS IoT topic name [default: cosmo]
"""
import serial
from docopt import docopt
from gevent import monkey

from cosmopusher.demo_stream import DemoStream
from cosmopusher.iot_pusher import IotPusher
from cosmopusher.n560reader import N560Reader
from cosmopusher.print_pusher import PrintPusher

monkey.patch_all()

arguments = docopt(__doc__)

if arguments['--demo']:
    stream = DemoStream()
else:
    stream = serial.Serial("/dev/serial0", baudrate=19200, timeout=120)

if arguments['--print']:
    pusher = PrintPusher()
else:
    pusher = IotPusher(arguments['--endpoint'], arguments['--root-ca'], arguments['--topic'])

reader = N560Reader(stream, pusher)
try:
    reader.run()
except KeyboardInterrupt:
    print("exiting")