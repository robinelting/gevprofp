import sys
import re
import pysrt

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
	tagged_sentences = []
	for line in text:
		if 'CUT TO:' in line:
			tagged_sentences.append('M|\t'+ line)
		elif 'ON THE SCREEN' in line:
			tagged_sentences.append('M|\t'+ line)
		elif 'IN THE CLOSET' in line:
			tagged_sentences.append('M|\t'+ line)
	return tagged_sentences

def c_tagger(text):
	tagged_sentences = []
	for item in text:
		tagged_sentences.append(re.findall(r'[A-Z]+$', item))
	return tagged_sentences


def main():
	with open(sys.argv[1], 'rt', encoding='utf8') as f:
		file_content = f.read()

	file_content = file_content.split('\n\n')
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
	s_tagged = []
	for line in preprocessed_subs:
		res1 = re.search(r'^INT', line)
		res2 = re.search(r'^EXT', line)
		if res1:
			s_tagged.append('S|\t' + res1.string)
		elif res2:
			s_tagged.append('S|\t' + res2.string)
	#print(s_tagged)

	# M-tags
	m_tagged = []
	for line in preprocessed_subs:
		res3 = re.search('ON THE|IN THE|CUT TO:', line)
		if res3:
			m_tagged.append('M|\t' + res3.string)

	#print(m_tagged)

if __name__ == "__main__":
	main()
