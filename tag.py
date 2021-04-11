import sys
import re
import pysrt
import nltk
from linecache import getline
from itertools import islice

def tokenizer(sentence):
	sentence = re.sub(r'[^\w\s]', " ", sentence)
	sentence = sentence.lower()
	return sentence


def tagger(content):
	tagged_sentences = []
	for line in content:
		scene = re.search(r'^ {5}INT\.|^ {5}EXT\.', line)
		meta1 = re.search(r'^ {5}ON THE|^ {5}IN THE|^ {5}CUT TO:', line)
		meta2 = re.search(r'^(\(.\))', line)
		character = re.search(r' {26}[A-Z]{3,}', line)
		descr = re.search(r'^ {5}[A-Za-z]', line)
		dialogue = re.search(r' {16}[A-Za-z ]{10,}', line)
		if scene:
			tagged_sentences.append('S|\t' + scene.string + '\n')
		elif meta1:
			tagged_sentences.append('M|\t' + meta1.string + '\n')
		elif character:
			tagged_sentences.append('C|\t\t' + character.string + '\n')
		elif descr:
			tagged_sentences.append('N|' + descr.string)
		elif dialogue:
			tagged_sentences.append('D|' + dialogue.string + '\n')
		else:
			tagged_sentences.append(' |' + line)
	return tagged_sentences


def main():
	with open(sys.argv[1], 'rt', encoding='utf8') as f:
		file_content = f.read()


	file_content = file_content.split('\n')
	#print(file_content)
	
	#print(preprocessed_subs)

	tags = tagger(file_content)
	print('\n'.join(tags))



if __name__ == "__main__":
	main()
