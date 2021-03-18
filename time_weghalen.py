import re

with open('mi.srt', 'r') as s:
    infile2 = s.readlines()

text = ''
for line in infile2:
    if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search(
            '^$', line) is None:
        text += ' ' + line.rstrip('\n')
    text = text.lstrip()

print(text)