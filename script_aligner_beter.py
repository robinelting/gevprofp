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

    file_content = re.sub('\. ','.\n\n',file_content)
    file_content = file_content.split('\n\n')
    preprocessed_subs = []
    non_processed_subs = []
    for line in file_content:
        line = re.sub(' +',' ',line)
        line = re.sub('\n', ' ', line)
        if line != '':
            non_processed_subs.append(line)
            line = tokenizer(line)
            preprocessed_subs.append(line)
    

#    print(preprocessed_subs, sep="\n")

    subs = pysrt.open(sys.argv[2], encoding='iso-8859-1')
    script_text = []
    script_time = []
    for sub in subs:
        sub_string = str(sub)
        sub_time = sub_string.split('\n')[1]
        sub_text = sub_string.split('\n')[2]
        script_text.append(tokenizer(sub_text))
        script_time.append(sub_time)

#    print(script_text)
#    print(script_time)

    aligned_script = {}
    list_sets_subs = []
    for prep_sub in preprocessed_subs:
        sub_set = set(re.split('\s+', prep_sub))
        list_sets_subs.append(sub_set)
#    print(list_sets_subs)

    for script, time in zip(script_text, script_time):
        script_set = set(re.split('\s+', script))
        resemblance_high = 0
        best_resemblance = ''
        for sub_set in list_sets_subs:
            resemblance = script_set.intersection(sub_set)
            resemblance_correct = len(resemblance) / len(script_set)
            if resemblance_correct > resemblance_high:
                resemblance_high = resemblance_correct
                best_resemblance = resemblance
                best_resemblance_index = list_sets_subs.index(sub_set)
        aligned_script[script] = non_processed_subs[best_resemblance_index], time

    for item in aligned_script:
        print(item)
        print(aligned_script[item])
        print('\n')

if __name__ == "__main__":
    main()
