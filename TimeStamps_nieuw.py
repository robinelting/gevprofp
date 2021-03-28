import re


def matcher(script, subtitles, timestamps, new_list):
    print(new_list)
    if len(script) == 1:
        return new_list

    for item in script:
        word2 = item.split()

        for i in range(len(subtitles)):
            indexer1 = subtitles.index(subtitles[i])
            indexer2 = script.index(item)
            word = subtitles[i]
            word = re.sub(r'[^\w\s]', '', word).lower()
            words = word.split()
            check = all(item in word2 for item in words)
            if check is True:
                new_list.append(item + " " + timestamps[i])
                print(new_list)
                return matcher(script[indexer2 + 1:], subtitles[indexer1 + 1:], timestamps[indexer1 + 1:], new_list)


def search(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def add_stamp(sentence, timestamps):
    if search("Come on, come on. She's been under too long.")(sentence):
        return timestamps[-1]


def tokenizer(sentence):
    sentence = re.sub(r'[^\w\s]', "", sentence)
    sentence = sentence.lower()
    return sentence


def main():
    with open('mi.txt', 'rt', encoding='utf8') as f:
        infile = f.read()
        infile_lst = infile.split('\n\n')

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
            # infile2.pop(indexes - 1)
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

    print(text)

    for i in range(len(text)):
        zin = text[i].split()
        if len(zin) >= 2:
            list_check.append(zin[0] + " " + zin[1])
        if len(zin) == 1:
            list_check.append(zin[0])


    lster = []
    lster2 = []
    for line in infile_lst:
        line = re.sub(' +', ' ', line)
        line = re.sub('\n', ' ', line)
        if line != '':
            lster.append(line)
    for line in lster:
        token = tokenizer(line)
        lster2.append(token)

    new_list2 = []

    yes = matcher(lster2, text, timestamps, new_list2)
    print(yes)


if __name__ == '__main__':
    main()
