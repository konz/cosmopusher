from unittest import TestCase

from io import BytesIO

from cosmopusher.bytes_reader import BytesReader


class BytesReaderTests(TestCase):

    def test_read_ascii_line(self):
        reader = BytesReader(BytesIO(b"bla bla\n"))

        self.assertEqual("bla bla", reader.readlines().__next__())

    def test_read_non_ascii_line(self):
        reader = BytesReader(BytesIO("blá blá".encode()))

        self.assertEqual("bl bl", reader.readlines().__next__())
