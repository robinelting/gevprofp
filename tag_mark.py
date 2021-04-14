import sys
import re
import pysrt
import nltk
import csv
import pandas
from collections import defaultdict

def tokenizer(sentence):
	sentence = re.sub(r'[^\w\s]', " ", sentence)
	sentence = sentence.lower()
	return sentence


def tagger(content):
	tagged_sentences = []
	for line in content:
		scene = re.search(r'INT\.|EXT\.', line)
		meta1 = re.search(r'^ {5}ON THE|^ {5}IN THE|CUT TO:|THE END|FINAL SHOOTING SCRIPT', line)
		meta2 = re.search(r'[A-Z]\:|  \([A-Za-z0-9 ]+\)', line)
		character = re.search(r' {26}[A-Z]{3,}', line)
		descr = re.search(r'^ {5}[A-Za-z]|^ {10}[A-Za-z]', line)
		dialogue = re.search(r' {16}[A-Za-z \.\'?!,]{10,}', line)
		if scene:
			tagged_sentences.append(['S', scene.string])
		elif meta1:
			tagged_sentences.append(['M', meta1.string])
		elif meta2:
			tagged_sentences.append(['M', meta2.string])
		elif character:
			tagged_sentences.append(['C', character.string])
		elif descr:
			tagged_sentences.append(['N', descr.string])
		elif dialogue:
			tagged_sentences.append(['D', dialogue.string])
		else:
			tagged_sentences.append(['?', line])
	return tagged_sentences


def dic_tagger(content):
	"""Searches for regex patterns and creates a dictionary with tagged lines
	:param content: line-splitted text
	"""
	dic_tag = dict()
	for line in content:
		scene = re.compile(r'INT\.|EXT\.')
		meta1 = re.search(r'^ {5}ON THE|^ {5}IN THE|CUT TO:|THE END|FINAL SHOOTING SCRIPT', line)
		meta2 = re.search(r'[A-Z]\:|  \([A-Za-z0-9 ]+\)', line)
		character = re.search(r' {26}[A-Z]{3,}', line)
		descr = re.search(r'^ {5}[A-Za-z]|^ {10}[A-Za-z]', line)
		dialogue = re.search(r' {16}[A-Za-z ]{10,}', line)
		
		scenes = re.findall(r'INT\.|EXT\.', line)
		characters = re.findall(r' {26}[A-Z]{3,}', line)
		if scenes:
			dic_tag[content.index(line)] = line
		elif characters:
			dic_tag[content.index(line)] = line

	return dic_tag


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


def script_aligner(tagged_sentences, subs_text, subs_time):
    """aligns subtitles, timestamps and script into a cohesive dictionary"""
#    sub_total = 0
#    sub_total_correct = 0
    for sub_text, time in zip(subs_text, subs_time):
        sub_set = set(re.split('\s+', sub_text))
        resemblance_high = 0
        best_resemblance = ''
        for script in tagged_sentences:
            script_set = set(re.split('\s+', script[1]))
            resemblance = sub_set.intersection(script_set)
            resemblance_correct = len(resemblance) / len(sub_set)
            if resemblance_correct > resemblance_high:
                resemblance_high = resemblance_correct
                best_resemblance = resemblance
                best_resemblance_index = tagged_sentences.index(script)
        tagged_sentences[best_resemblance_index].append(sub_text)
        tagged_sentences[best_resemblance_index].append(time)
        print(tagged_sentences)
    return tagged_sentences

#        aligned_script[non_processed_script[best_resemblance_index]] = sub_text, time
#        sub_total += len(sub_set)
#        sub_total_correct += len(best_resemblance)
#    print("total amount of words in subtitles: {}\n"
#          "total amount of words that match between script and subs: {}\n"
#          "percentage of matches between script and subs: {}%\n"
#           .format(sub_total, sub_total_correct, sub_total_correct/sub_total*100))


def main():
	with open(sys.argv[1], 'rt', encoding='utf8') as f:
		file_content = f.read()

	file_content = file_content.split('\n')

	tag_dic = dic_tagger(file_content)
	sents = tagger(file_content)
	subtitles, timestamps = subtitles_preprocessing()
	sents = script_aligner(sents, subtitles, timestamps)
#	print(sents)
	
#	for item in sents:
#		#print(item[1])
#		for subtitle in subtitles:
#			if subtitle in item[1]:
#				item.append(subtitle)


	df = pandas.DataFrame(sents)
	
	df.to_csv(r'./output.csv', index=False, header=True)

if __name__ == "__main__":
	main()
