import sys
import pysrt
import re

with open('mi.txt', 'rt', encoding='utf8') as f:
    infile = f.read()
    infile = infile.split()

with open('mi.srt', 'r') as s:
    infile2 = s.readlines()

text = []
sentence = ''
sentence2 = ''
timestamps = []


for word in infile2:
    indexes = infile2.index(word)
    if word[0] == "0":
        timestamps.append(word.strip())
        infile2.pop(indexes)
        #infile2.pop(indexes - 1)
    else:
        pass

hoi = ' '.join(infile2)
yes = hoi.split()
indexen = 1

for word in yes:
    if str(word) == str(indexen):
        indexen = indexen + 1
        text.append(sentence)
        sentence = sentence2
        if text[-1] == '':
            text.pop(-1)

    elif word[0] != str(indexen):
        if word[0] == "<" and word[-1] != ">":
            new = word[3:]
            if word[-1] == ">":
                new = new[:-4]
                sentence = sentence + new + " "
            elif word[3] == "-":
                new = new[1:]
                sentence = sentence + new + " "
            else:
                sentence = sentence + new + " "

        elif word[-1] == ">" and word[0] == "<":
            new = word[3:]
            newer = new[:-4]
            sentence = sentence + newer + " "

        elif word[-1] == ">" and word[-2] == "i" and word[0] != "<":
            new = word[:-4]
            sentence = sentence + new + " "

        else:
            sentence = sentence + word + " "

list_check = []
text.append(sentence)


for i in range(len(text)):
    zin = text[i].split()
    if len(zin) >= 2:
        list_check.append(zin[0] + " " + zin[1])
    if len(zin) == 1:
        list_check.append(zin[0])

finder = " ".join(list_check)
finder = finder.split()


print(text)
print(timestamps)
print(len(timestamps))
print(list_check)
print(len(list_check))


