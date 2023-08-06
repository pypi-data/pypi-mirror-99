
import re
from subsparser.constants import BYTE_ORDER_MARK
from subsparser.constants import OVERRIDE_SEQUENCE

class BaseReader:
    EXT = None
    HEADER = None

    def __init__(
        self, start=None, end=None, text=None, style=None, layout=None
    ):
        self.start = start
        self.end = end
        self.text = text
        self.style = style
        self.layout = layout

    def prepare_text(
        lines, keep_unknown_html_tags=False, remove_override_sequence=True
    ):
        # Handle the "happy" empty subtitle case, which is timestamp line followed by blank line(s)
        # followed by number line and timestamp line of the next subtitle. Fixes issue #11.
        if (len(lines) >= 2
                and all(re.match("\s*$", line) for line in lines[:-1])
                and re.match("\s*\d+\s*$", lines[-1])):
            return ""

        # Handle the general case.
        s = "".join(lines).strip()
        s = re.sub(r"\n+ *\d+ *$", "", s) # strip number of next subtitle
        s = re.sub(r"< *i *>", r"{\\i1}", s)
        s = re.sub(r"< */ *i *>", r"{\\i0}", s)
        s = re.sub(r"< *s *>", r"{\\s1}", s)
        s = re.sub(r"< */ *s *>", r"{\\s0}", s)
        s = re.sub(r"< *u *>", "{\\\\u1}", s) # not r" for Python 2.7 compat, triggers unicodeescape
        s = re.sub(r"< */ *u *>", "{\\\\u0}", s)
        if not keep_unknown_html_tags:
            s = re.sub(r"< */? *[a-zA-Z][^>]*>", "", s) # strip other HTML tags
        s = re.sub(r"\n", r"\\N", s) # convert newlines
        if remove_override_sequence:
            s = OVERRIDE_SEQUENCE.sub("", s)

        return s