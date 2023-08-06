import re
from subsparser.times import Times
from subsparser.constants import TIMESTAMP
from subsparser.readers.base import BaseReader


class SRTReader(BaseReader):

    @staticmethod
    def parse(lines):
        timestamps = [] # (start, end)
        following_lines = [] # contains lists of lines following each timestamp

        for line in lines:
            stamps = TIMESTAMP.findall(line)
            if len(stamps) == 2: # timestamp line
                start, end = map(Times.from_timestamp, stamps)
                timestamps.append((start, end))
                following_lines.append([])
            else:
                if timestamps:
                    following_lines[-1].append(line)


        contents = [
            SRTReader(timestamp[0], timestamp[1], SRTReader.prepare_text(lines))
            for timestamp, lines in zip(timestamps, following_lines)
        ]
        return contents