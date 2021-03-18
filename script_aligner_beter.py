import sys
import re
import pysrt

def tokenizer(sentence):
    sentence = re.sub(r'[^\w\s]', " ", sentence)
    sentence = sentence.lower()
    return sentence

def main():
    with open(sys.argv[1], 'rt', encoding='utf8') as f:
        file_content = f.read()

    file_content = file_content.split('\n\n')
    preprocessed_subs = []
    for line in file_content:
        line = re.sub(' +',' ',line)
        line = re.sub('\n', ' ', line)
        if line != '':
#            line = tokenizer(line)
            preprocessed_subs.append(line)
    

    print(preprocessed_subs, sep="\n")

    subs = pysrt.open(sys.argv[2], encoding='iso-8859-1')
#    for sub in subs:
#        print(sub.text)
#        print()
    


if __name__ == "__main__":
    main()
