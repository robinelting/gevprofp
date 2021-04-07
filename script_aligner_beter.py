import sys
import re
import pysrt


def tokenizer(sentence):
    """cleans up the sentence and makes it lowercase"""
    sentence = re.sub(r'[^\w\s]', " ", sentence)
    sentence = sentence.lower()
    return sentence


def script_preprocessing():
    """opens up script (.txt) and returns two lists split by two newlines"""
    """returns a 'clean' list and a regular list"""
    with open(sys.argv[1], 'rt', encoding='utf8') as f:
        file_content = f.read()

    file_content = re.sub('\. ','.\n\n',file_content)
    file_content = file_content.split('\n\n')
    preprocessed_script = []
    non_processed_script = []
    for line in file_content:
        line = re.sub(' +',' ',line)
        line = re.sub('\n', ' ', line)
        if line != '':
            non_processed_script.append(line)
            line = tokenizer(line)
            preprocessed_script.append(line)
    return non_processed_script, preprocessed_script


def subtitles_preprocessing():
    """opens up subtitles (.srt) and returns 2 lists"""
    """one with only subtitles and the other with timestamps"""
    subs = pysrt.open(sys.argv[2], encoding='iso-8859-1')
    subs_text = []
    subs_time = []
    for sub in subs:
        sub_string = str(sub)
        sub_time = sub_string.split('\n')[1]
        sub_text = sub_string.split('\n')[2]
        subs_text.append(tokenizer(sub_text))
        subs_time.append(sub_time)
    return subs_text, subs_time


def script_to_sets(preprocessed_script):
    """takes preprocessed script and makes a list of all sentences"""
    """split into sets"""
    list_sets_script = []
    for prep_script in preprocessed_script:
        script_set = set(re.split('\s+', prep_script))
        list_sets_script.append(script_set)
    return list_sets_script


def script_aligner(subs_text, subs_time, list_sets_script, non_processed_script):
    """aligns subtitles, timestamps and script into a cohesive dictionary"""
    aligned_script = {}
    for sub_text, time in zip(subs_text, subs_time):
        sub_set = set(re.split('\s+', sub_text))
        resemblance_high = 0
        best_resemblance = ''
        for script_set in list_sets_script:
            resemblance = sub_set.intersection(script_set)
            resemblance_correct = len(resemblance) / len(sub_set)
            if resemblance_correct > resemblance_high:
                resemblance_high = resemblance_correct
                best_resemblance = resemblance
                best_resemblance_index = list_sets_script.index(script_set)
        aligned_script[sub_text] = non_processed_script[best_resemblance_index], time

    return aligned_script


def main():
    non_processed_script, preprocessed_script = script_preprocessing()
    list_sets_script = script_to_sets(preprocessed_script)
    subs_text, subs_time = subtitles_preprocessing()

    aligned_script = script_aligner(subs_text, subs_time, list_sets_script, non_processed_script)

    for item in aligned_script:
        print(item)
        print(aligned_script[item])
        print('\n')


if __name__ == "__main__":
    main()
