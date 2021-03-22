import sys
import re
import pysrt

def tokenizer(sentence):
    sentence = re.sub(r'[^\w\s]', " ", sentence)
    sentence = sentence.lower()
    return sentence


def s_tagger(text):
    tagged_sentences = []
    for line in text:
        for mark in ['EXT.', 'INT.']:
            if mark in line:
                tagged_sentences.append('S|\t'+ line)
    return tagged_sentences

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
    
#    print(preprocessed_subs)
    
    s_tagged = s_tagger(preprocessed_subs)
    
   


if __name__ == "__main__":
    main()
