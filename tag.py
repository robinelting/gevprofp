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
		if 'EXT.' in line or 'INT.' in line:
			tagged_sentences.append('S|\t' + line)
		elif 'CUT TO:' in line or 'ON THE SCREEN' in line or 'IN THE CLOSET' in line:
			tagged_sentences.append('M|\t' + line)
	return tagged_sentences


def m_tagger(text):
	m_tagged = []
	for line in text:
		res3 = re.search('ON THE|IN THE|CUT TO:', line)
		if res3:
			m_tagged.append('M|\t' + res3.string)
	return m_tagged


def s_tagger(text):
	s_tagged = []
	for line in text:
		res1 = re.search(r'^INT.|^EXT.', line)
		if res1:
			s_tagged.append('S|\t' + res1.string)
	return s_tagged


def n_tagger(text):
	pl = '\n'.join(text)
	n_tagged = []
	for line in pl:
		if 'EXT.' in line:
			n_tagged.append("".join(islice(pl,4)))

	return n_tagged


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

	# S-tags
	s_tags = s_tagger(preprocessed_subs)
	#print(s_tags)

	# M-tags
	m_tags = m_tagger(preprocessed_subs)
	#print(m_tags)
	
	# N-tags
	n_tags = n_tagger(preprocessed_subs)
	#print(n_tags)

	preprocessed_text = '\n'.join(preprocessed_subs)
	for line in preprocessed_subs:
		if 'EXT.' in line:
			#print(line)
			print(''.join(islice(preprocessed_text,4)))




if __name__ == "__main__":
	main()
