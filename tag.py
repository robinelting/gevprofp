import sys
import re
import pysrt
import nltk
from linecache import getline
from itertools import islice
import csv
import json

def tokenizer(sentence):
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


def main():
	with open(sys.argv[1], 'rt', encoding='utf8') as f:
		file_content = f.read()

	file_content = file_content.split('\n')

	tag_dic = dic_tagger(file_content)

	with open('output.csv', 'w') as output:
		writer = csv.writer(output)
		for key, value in tag_dic.items():
			writer.writerow([key, value])


if __name__ == "__main__":
	main()
