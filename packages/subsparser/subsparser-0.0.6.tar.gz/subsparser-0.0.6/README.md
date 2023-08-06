# subtitle file parser

it support txt and srt file parsing


from subsparser.subtitle import SubtitleFile

s = SubtitleFile(path=File Path)
s.detect_encoding().read().parse()
s.print()

you can use s.data for list of parsed content objects

for ins in s.data:
    print(ins.start, ins.end, ins.text)

if you want to add your custom subtitle files parsing logic.
Feel free to add raise a PR