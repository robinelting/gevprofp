import sys
import re
import pysrt
import csv
import tkinter as tk
from tkinter import simpledialog
from collections import defaultdict


def tokenizer(sentence):
    """cleans up the sentence and makes it lowercase"""
    sentence = re.sub(r'[^\w\s]', " ", sentence)
    sentence = sentence.lower()
    return sentence


def dic_tagger(content):
    """Searches for regex patterns and creates a dictionary with tagged lines
    :param content: line-splitted text
    """
    dic_tag = dict()
    for line in content:
        scene = re.search(r'INT\.|EXT\.', line)
        meta1 = re.search(r'^ {5}ON THE|^ {5}IN THE|CUT TO:|THE END|FINAL SHOOTING SCRIPT', line)
        meta2 = re.search(r'[A-Z]\:|  \([A-Za-z0-9 ]+\)', line)
        character = re.search(r' {26}[A-Z]{3,}', line)
        descr = re.search(r'^ {5}[A-Za-z]', line)
        dialogue = re.search(r' {16}[A-Za-z ]{10,}', line)
        if scene:
            dic_tag[scene.string] = 'S'
        elif meta1:
            dic_tag[meta1.string] = 'M'
        elif meta2:
            dic_tag[meta2.string] = 'M'
        elif character:
            dic_tag[character.string] = 'C'
        elif descr:
            dic_tag[descr.string] = 'N'
        elif dialogue:
            dic_tag[dialogue.string] = 'D'
        else:
            dic_tag[line] = ' '

    new_dic = dict()
    for k, v in dic_tag.items():
        k2 = re.sub(r' {3,}', '', k)
        if k2 not in new_dic:
            new_dic[k2] = v

    return new_dic


def script_preprocessing(lister, file_content):
    """opens up script (.txt) and returns two lists split by two newlines"""
    """returns a 'clean' list and a regular list"""

    file_content = file_content.split('\n')
    preprocessed_script = []
    non_processed_script = []

    for line in lister:
        non_processed_script.append(line)
        line = re.sub(' +', ' ', line)
        line = re.sub('\n', ' ', line)
        line = tokenizer(line)
        preprocessed_script.append(line)
    return non_processed_script, preprocessed_script


def subtitles_preprocessing():
    """opens up subtitles (.srt) and returns 2 lists"""
    """one with only subtitles and the other with timestamps"""
    subs = pysrt.open('mi.srt', encoding='iso-8859-1')
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
    with open("mi.txt", 'rt', encoding='utf8') as f:
        file_content = f.read()

    subs = pysrt.open('mi.srt', encoding='iso-8859-1')

    file_content1 = file_content.split('\n')
    hes = dic_tagger(file_content1)

    lister = []
    print(hes)

    for key in hes:
        lister.append(key)

    non_processed_script, preprocessed_script = script_preprocessing(lister, file_content)
    list_sets_script = script_to_sets(preprocessed_script)
    subs_text, subs_time = subtitles_preprocessing()

    aligned_script = script_aligner(subs_text, subs_time, list_sets_script, non_processed_script)

    new_dict = {}

    for k in aligned_script.items():
        yes = k[1]
        # print(yes[0])
        if hes[yes[0]]:
            hes[yes[0]] = [hes[yes[0]], yes[1]]
        else:
            pass
            #new_dict[k] =



   # print(hes)
    #print(hes.keys())


if __name__ == "__main__":
    main()
