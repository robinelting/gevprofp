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
		scene = re.search(r'^INT.|^EXT.', line)
		meta = re.search('ON THE|IN THE|CUT TO:', line)
		character = re.search(r'[A-Z]{3,}|[A-Z] {3,}', line)
		if scene:
			tagged_sentences.append('S|\t' + scene.string)
		elif meta:
			tagged_sentences.append('M|\t' + meta.string)
		elif character:
			tagged_sentences.append('C|\t' + character.group(0))
	return tagged_sentences


def main():
	with open(sys.argv[1], 'rt', encoding='utf8') as f:
		file_content = f.read()

	file_content = file_content.split('\n')
	preprocessed_subs = []
	for line in file_content:
		line = re.sub(' +',' ',line)
		line = re.sub('\n', ' ', line)
		line = re.sub('  ', '', line)
		line = re.sub(r'^ ', '', line)
		if line != '':
#            line = tokenizer(line)
			preprocessed_subs.append(line)
	
	#print(preprocessed_subs)

	tags = tagger(preprocessed_subs)
	print('\n'.join(tags))

	
	preprocessed_text = '\n'.join(preprocessed_subs)





if __name__ == "__main__":
	main()
