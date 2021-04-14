import sys
import re
import pysrt
import nltk
import csv

def tokenizer(sentence):
	sentence = re.sub(r'[^\w\s]', " ", sentence)
	sentence = sentence.lower()
	return sentence


def tagger(content):
	tagged_sentences = []
	dic_tag = dict()
	for line in content:
		scene = re.search(r'INT\.|EXT\.', line)
		meta1 = re.search(r'^ {5}ON THE|^ {5}IN THE|CUT TO:|THE END|FINAL SHOOTING SCRIPT', line)
		meta2 = re.search(r'[A-Z]\:|  \([A-Za-z0-9 ]+\)', line)
		character = re.search(r' {26}[A-Z]{3,}', line)
		descr = re.search(r'^ {5}[A-Za-z]|^ {10}[A-Za-z]', line)
		dialogue = re.search(r' {16}[A-Za-z \.\'?!,]{10,}', line)
		if scene:
			tagged_sentences.append('S|\t' + scene.string)
		elif meta1:
			tagged_sentences.append('M|\t' + meta1.string)
		elif meta2:
			tagged_sentences.append('M|\t' + meta2.string)
		elif character:
			tagged_sentences.append('C|\t\t' + character.string)
		elif descr:
			tagged_sentences.append('N|\t' + descr.string)
		elif dialogue:
			tagged_sentences.append('D|\t' + dialogue.string)
		else:
			tagged_sentences.append(' |\t' + line)
	return tagged_sentences



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
		descr = re.search(r'^ {5}[A-Za-z]|^ {10}[A-Za-z]', line)
		dialogue = re.search(r' {16}[A-Za-z ]{10,}', line)
		if scene:
			dic_tag[content.index(line)] = tuple(['S', scene.string])
		elif meta1:
			dic_tag[content.index(line)] = tuple(['M', meta1.string])
		elif meta2:
			dic_tag[content.index(line)] = tuple(['M', meta2.string])
		elif character:
			dic_tag[content.index(line)] = tuple(['C', character.string])
		elif descr:
			dic_tag[content.index(line)] = tuple(['N', descr.string])
		elif dialogue:
			dic_tag[content.index(line)] = tuple(['D', dialogue.string])
		else:
			dic_tag[content.index(line)] = tuple([' ', line])
	
	new_dic = dict()
	for k, v in dic_tag.items():
		for value in v:
			value = re.sub(r' {3,}', '', value)
			if v not in new_dic:
				new_dic[k] = v

	return dic_tag


def main():
	with open(sys.argv[1], 'rt', encoding='utf8') as f:
		file_content = f.read()

	file_content = file_content.split('\n')

	tag_dic = dic_tagger(file_content)
	sents = tagger(file_content)

	print(tag_dic)
	#print('\n'.join(sents))

	with open('output.csv', 'w') as output:
		writer = csv.writer(output)
		for key, value in tag_dic.items():
			writer.writerow([key, value])


if __name__ == "__main__":
	main()
