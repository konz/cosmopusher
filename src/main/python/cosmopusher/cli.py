#!/usr/bin/env python

"""Cosmopusher. Reads and parses data from N560 pulse oxymeters and sends it to AWS IoT.

Usage:
  cpusher.py (-h | --help)
  cpusher.py [-d] [-X] [--endpoint=ENDPOINT] --root-ca=FILE [--topic=TOPIC_NAME]
  cpusher.py (-p | --print) [-d] [-X]

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
import os

import serial
from docopt import docopt

from cosmopusher.bytes_reader import BytesReader
from cosmopusher.demo_stream import DemoStream
from cosmopusher.iot_pusher import IotPusher
from cosmopusher.n560reader import N560Reader
from cosmopusher.print_pusher import PrintPusher


def main():
    arguments = docopt(__doc__)

    configure_logging(arguments)

    input_stream = configure_input_stream(arguments)
    pusher = configure_pusher(arguments)
    reader = N560Reader(input_stream, pusher)
    try:
        reader.run()
    except KeyboardInterrupt:
        print("exiting")


def configure_pusher(arguments):
    if arguments['--print']:
        return PrintPusher()
    else:
        if arguments['--endpoint']:
            iot_endpoint = arguments['--endpoint']
        elif os.environ['IOT_ENDPOINT']:
            iot_endpoint = os.environ['IOT_ENDPOINT']
        else:
            print("Either --endpoint or environment varible IOT_ENPOINT required")
            exit(1)

        return IotPusher(iot_endpoint, arguments['--root-ca'], arguments['--topic'])


def configure_input_stream(arguments):
    if arguments['--demo']:
        return DemoStream()
    else:
        return BytesReader(serial.Serial("/dev/serial0", baudrate=19200, timeout=None))


def configure_logging(arguments):
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if arguments['-X']:
        logging.basicConfig(level=logging.DEBUG, format=log_format)
    else:
        logging.basicConfig(level=logging.WARNING, format=log_format)