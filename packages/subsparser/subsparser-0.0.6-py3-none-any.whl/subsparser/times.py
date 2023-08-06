class Times:

    def __init__(self, h=0, m=0, s=0, ms=0, fr=0):
        self.h = h
        self.m = m
        self.s = s
        self.ms = ms
        self.fr = fr

    @classmethod
    def from_timestamp(cls, groups):
        h, m, s, ms = map(int, groups)
        return Times(h, m, s, ms, 0)

    @classmethod
    def from_frame_timestamp(cls, groups):
        h, m, s, fr = map(int, groups)
        return Times(h, m, s, 0, fr)

    def __str__(self):
        return "%02d:%02d:%02d:%02d,fr:%02d" % (
            self.h, self.m, self.s, self.ms, self.fr
        )

    def milliseconds(self):
        ms = self.ms
        ms += self.s * 1000
        ms += self.m * 60000
        ms += self.h * 3600000
        return ms

    def values(self):
        return (self.h, self.m, self.s, self.ms, self.fr)