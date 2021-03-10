import sys
import re
import pysrt

def main():
    with open(sys.argv[1], 'rt', encoding='utf8') as f:
        file_content = f.read()
    file_content = file_content.split('\n')
    preprocessed_subs = []

    for line in file_content:
        line = re.sub(' +',' ',line)
        if line != '':
            preprocessed_subs.append(line)
    

    print(preprocessed_subs, sep="\n")

    subs = pysrt.open(sys.argv[2], encoding='iso-8859-1')
#    for sub in subs:
#        print(sub.text)
#        print()
    


if __name__ == "__main__":
    main()
