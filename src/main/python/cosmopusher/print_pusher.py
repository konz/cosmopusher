class PrintPusher:

    def push(self, event_type, payload):
        print("{}: {}".format(event_type, payload))
