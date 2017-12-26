from random import randint

import gevent
from gevent import Greenlet


class PrintLine(Greenlet):

    def __init__(self, payload):
        Greenlet.__init__(self)
        self.payload = payload
        self.delayed = 0

    def _run(self):
        try:
            self.send()
        except Exception:
            gevent.sleep(1)
            self.delayed += 1
            self._run()

    def send(self):
        if randint(0, 1) == 0:
            raise Exception
        else:
            print("DELAYED: {}: {}".format(self.delayed, self.payload))


class PrintPusher(Greenlet):

    def push(self, _, payload):
        PrintLine.spawn(payload)
