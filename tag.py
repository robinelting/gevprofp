import sys
import re
import pysrt
import nltk
import csv
import pandas
from collections import defaultdict
from char import subtitles_preprocessing

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



def main():
	with open(sys.argv[1], 'rt', encoding='utf8') as f:
		file_content = f.read()

	file_content = file_content.split('\n')

	tag_dic = dic_tagger(file_content)
	sents = tagger(file_content)
	subtitles, timestamps = subtitles_preprocessing()
	
	for item in sents:
		#print(item[1])
		for subtitle in subtitles:
			if subtitle in item[1]:
				item.append(subtitle)


	df = pandas.DataFrame(sents)
	
	df.to_csv(r'./output.csv', index=False, header=True)

if __name__ == "__main__":
	main()
