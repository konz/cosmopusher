from io import StringIO
from unittest import TestCase, mock

from hamcrest import match_equality, all_of, has_entry, matches_regexp, has_key, not_

from cosmopusher.n560reader import N560Reader

TIMESTAMP_REGEX = '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}$'


class N560ReaderTests(TestCase):

    def test_sat_and_pulse(self):
        pusher = mock.Mock()
        data = StringIO("18-Dec-17 22:01:33    99      66      49")

        reader = N560Reader(data, pusher)
        reader.run()

        pusher.push.assert_called_with(
            "data",
            match_equality(
                all_of(
                    has_entry('time', matches_regexp(TIMESTAMP_REGEX)),
                    has_entry('spO2', 99),
                    has_entry('pulse', 66)
                )))

    def test_settings(self):
        pusher = mock.Mock()
        data = StringIO("N-560    VERSION 1.61.00    CRC:XXXX  SpO2 Limit: 94-100%    PR Limit: 50-170BPM")

        reader = N560Reader(data, pusher)
        reader.run()

        pusher.push.assert_called_with(
            "settings",
            match_equality(
                all_of(
                    has_entry('time', matches_regexp(TIMESTAMP_REGEX)),
                    has_entry('spO2LowerLimit', 94),
                    has_entry('spO2UpperLimit', 100),
                    has_entry('pulseLowerLimit', 50),
                    has_entry('pulseUpperLimit', 170)
                )))

    def test_no_values(self):
        pusher = mock.Mock()
        data = StringIO("29-Dec-17 07:19:29   ---     ---     ---    SD          AS")

        N560Reader(data, pusher).run()

        pusher.push.assert_called_with(
            "data",
            match_equality(
                all_of(
                    has_entry('time', matches_regexp(TIMESTAMP_REGEX)),
                    not_(has_key('spO2')),
                    not_(has_key('pulse'))
                )))


    def test_non_parseable_line(self):
        pusher = mock.Mock()
        reader = N560Reader(StringIO("this does not make any sense"), pusher)
        reader.run()

        pusher.assert_not_called()

    def test_stops(self):
        pusher = mock.Mock()
        reader = N560Reader(StringIO("18-Dec-17 22:01:33    99      66      49"), pusher)
        reader.stop()

        reader.run()

        pusher.assert_not_called()