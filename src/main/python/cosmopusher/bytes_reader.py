class BytesReader:

    def __init__(self, byte_stream):
        self.byte_stream = byte_stream

    def readlines(self):
        while True:
            yield self.byte_stream.readline().decode("ascii").rstrip()
