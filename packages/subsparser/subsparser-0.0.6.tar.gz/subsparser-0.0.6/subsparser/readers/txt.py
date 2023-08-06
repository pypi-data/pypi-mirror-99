
import re
from subsparser.times import Times
from subsparser.constants import TXT_TIMESTAMP
from subsparser.constants import TIMESTAMP_WITH_FRAME
from subsparser.readers.base import BaseReader

class TXTReader(BaseReader):

    @staticmethod
    def parse(lines):

        timestamps = [] # (start, end)
        following_lines = [] # contains lists of lines following each timestamp

        for line in lines:
            stamps = TIMESTAMP_WITH_FRAME.findall(line)
            if len(stamps) == 2: # timestamp line
                start, end = map(Times.from_frame_timestamp, stamps)
                timestamps.append((start, end))
                following_lines.append([re.sub(TXT_TIMESTAMP, "", line)])

        contents = [
            TXTReader(timestamp[0], timestamp[1], TXTReader.prepare_text(lines))
            for timestamp, lines in zip(timestamps, following_lines)
        ]
        return contents