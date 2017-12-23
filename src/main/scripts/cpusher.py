#!/usr/bin/env python

"""Cosmopusher. Reads and parses data from N560 pulse oxymeters and sends it to AWS SNS topics.

Usage:
  cpusher.py (-h | --help)
  cpusher.py (-d | --demo)
  cpusher.py [-d] --iot --endpoint=ENDPOINT --root-ca=FILE [--topic=TOPIC_NAME]

Options:
  -h --help                 Show this screen.
  -d --demo                 Send some demo data.
  --iot                     Send data to AWS IoT, IAM access credentials required. Requires additional options:
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

if __name__ == '__main__':
    monkey.patch_all()

    arguments = docopt(__doc__)

    if arguments['--demo']:
        stream = DemoStream()
    else:
        stream = serial.Serial("/dev/serial0", timeout=120)

    if arguments['--iot']:
        pusher = IotPusher(arguments['--endpoint'], arguments['--root-ca'], arguments['--topic'])
    else:
        pusher = PrintPusher()

    reader = N560Reader(stream, pusher)
    try:
        reader.run()
    except KeyboardInterrupt:
        print("exiting")
