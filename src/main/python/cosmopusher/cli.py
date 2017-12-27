#!/usr/bin/env python

"""Cosmopusher. Reads and parses data from N560 pulse oxymeters and sends it to AWS IoT.

Usage:
  cpusher.py (-h | --help)
  cpusher.py [-d] [-X] --endpoint=ENDPOINT --root-ca=FILE [--topic=TOPIC_NAME]
  cpusher.py (-p | --print) [-d]

Options:
  -h --help                 Show this screen.
  -d --demo                 Send some demo data.
  -p --print                Instead of sending it to IoT, just print out the data.
                            (together with some simulation of delay)
  -X                        Enable debug logging
  --endpoint=HOSTNAME       AWS IoT endpoint
  --root-ca=FILE            AWS IoT root certificate file
  --topic=TOPIC_NAME        AWS IoT topic name [default: cosmo]
"""
import logging

import serial
from docopt import docopt
from gevent import monkey

from cosmopusher.bytes_reader import BytesReader
from cosmopusher.demo_stream import DemoStream
from cosmopusher.iot_pusher import IotPusher
from cosmopusher.n560reader import N560Reader
from cosmopusher.print_pusher import PrintPusher

monkey.patch_all()


def main():
    arguments = docopt(__doc__)

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if arguments['-X']:
        logging.basicConfig(level=logging.DEBUG, format=log_format)
    else:
        logging.basicConfig(level=logging.WARNING, format=log_format)

    if arguments['--demo']:
        stream = DemoStream()
    else:
        stream = BytesReader(serial.Serial("/dev/serial0", baudrate=19200, timeout=120))

    if arguments['--print']:
        pusher = PrintPusher()
    else:
        pusher = IotPusher(arguments['--endpoint'], arguments['--root-ca'], arguments['--topic'])

    reader = N560Reader(stream, pusher)
    try:
        reader.run()
    except KeyboardInterrupt:
        print("exiting")