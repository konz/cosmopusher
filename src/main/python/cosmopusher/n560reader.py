import logging
import re
from datetime import datetime

import gevent

DATA_REGEX = re.compile('^(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2})\s+(\d+|---)\*?\s+(\d+|---)\*?\s+(\d+|---)(.*)$')
SETTINGS_REGEX = re.compile('^(\S+)\s+VERSION (\S+).*?SpO2 Limit: (\d+)-(\d+)%\s+PR Limit: (\d+)-(\d+)BPM$')

LOGGER = logging.getLogger('cosmopusher')


class N560Reader:

    def __init__(self, text_stream, pusher):
        self.stream = text_stream
        self.running = True
        self.pusher = pusher

    def run(self):
        for line in self.stream.readlines():
            if not (self.running and line):
                break
            self.process_line(line)

        gevent.wait()
        LOGGER.info("no more data - exiting")

    def process_line(self, line):
        data_match = DATA_REGEX.match(line)
        settings_match = SETTINGS_REGEX.match(line)
        time = datetime.utcnow().isoformat()

        if data_match:
            payload = {'time': time}
            payload = self.add_int_value(payload, 'spO2', data_match, 2)
            payload = self.add_int_value(payload, 'pulse', data_match, 3)

            self.pusher.push("data", payload)

        elif settings_match:
            sp_o2_lower_limit = int(settings_match.group(3))
            sp_o2_upper_limit = int(settings_match.group(4))
            pulse_lower_limit = int(settings_match.group(5))
            pulse_upper_limit = int(settings_match.group(6))

            self.pusher.push("settings", {
                'time': time,
                'spO2LowerLimit': sp_o2_lower_limit,
                'spO2UpperLimit': sp_o2_upper_limit,
                'pulseLowerLimit': pulse_lower_limit,
                'pulseUpperLimit': pulse_upper_limit
            })

    @staticmethod
    def add_int_value(payload, key, matcher, group):
        try:
            payload[key] = int(matcher.group(group))
        except ValueError:
            pass
        return payload

    def stop(self):
        self.running = False
