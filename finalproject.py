import sys
import re
import pysrt
import nltk
import csv
import pandas
import argparse
from collections import defaultdict

def tokenizer(sentence):
	sentence = re.sub(r'[^\w\s]', " ", sentence)
	sentence = sentence.lower()
	return sentence


def tagger(content):
	"""Searches for regex patterns and returns a list with the first element
	being the tag and the second element being the script text.
	:param content: line-splitted text
	"""
	tagged_sentences = []
	for line in content:
		scene = re.search(r'int\.|int\.', line)
		meta1 = re.search(r'^ {5}ON THE|^ {5}IN THE|CUT TO:|THE END|FINAL SHOOTING SCRIPT|  \([A-Za-z0-9 ]+\)|[A-Z]\:', line)
		meta2 = re.search(r'[A-Z]\:|  \([A-Za-z0-9 ]+\)', line)
		character = re.search(r' {26}[A-Z]{3,}', line)
		descr = re.search(r'^ {5}[A-Za-z]|^ {10}[A-Za-z]', line)
		dialogue = re.search(r' {16}[A-Za-z \.\'?!,]{10,}', line)
		if scene:
			tagged_sentences.append(['S', scene.string])
		elif meta1:
			tagged_sentences.append(['M', meta1.string])
		#elif meta2:
		#	tagged_sentences.append(['M', meta2.string])
		elif character:
			tagged_sentences.append(['C', character.string])
		elif descr:
			tagged_sentences.append(['N', descr.string])
		elif dialogue:
			tagged_sentences.append(['D', dialogue.string])
		else:
			tagged_sentences.append([' ', line])
	return tagged_sentences


def subtitles_preprocessing(args):
	"""opens up subtitles (.srt) and returns 2 lists
	one with only subtitles and the other with timestamps
	:param args: argparse arguments
	"""
	subs = pysrt.open(args.subtitles, encoding='iso-8859-1')
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
	"""aligns subtitles, timestamps and script into a list
	:param tagged_sentences: list of tagged script sentences
	:param subs_text: preprocessed subtitles
	:param subs_time: preprocessed timestamps
	"""
	sub_total = 0
	sub_total_correct = 0
	for sub_text, time in zip(subs_text, subs_time):
		sub_set = set(re.split(r'\s+', sub_text))
		resemblance_high = 0
		best_resemblance = ''
		for script in tagged_sentences:
			if script[0] == 'D':
				script[1] = script[1].lower()
				script_set = set(re.split(r'\s+', script[1]))
				resemblance = sub_set.intersection(script_set)
				resemblance_correct = len(resemblance) / len(sub_set)
				if resemblance_correct > 0.6:
					if resemblance_correct > resemblance_high:
						resemblance_high = resemblance_correct
						best_resemblance = resemblance
						best_resemblance_index = tagged_sentences.index(script)
						tagged_sentences[best_resemblance_index].append(sub_text)
						tagged_sentences[best_resemblance_index].append(time)


		sub_total += len(sub_set)
		sub_total_correct += len(best_resemblance)
	print("Total amount of words in subtitles: {}\n"
	"Total amount of words that match between script and subtitles: {}\n"
	"Percentage of matches between script and subtitles: {}%\n"
	.format(sub_total, sub_total_correct, sub_total_correct/sub_total*100))
	return tagged_sentences


def main(argv):
	# Add arguments and parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("script")
	parser.add_argument("subtitles")
	parser.add_argument("output_file")
	args = parser.parse_args()

	# Print introduction message
	print('Aligning script and subtitles...')

	# Open script file
	with open(args.script, 'rt', encoding='utf8') as f:
		file_content = f.read()

	# Split script file on newline characters
	file_content = file_content.split('\n')

	# Obtain list tagged sentences
	sentences_tagged = tagger(file_content)

	# Obtain preprocessed subtitles and timestamps
	subtitles, timestamps = subtitles_preprocessing(args)

	# Obtain list of tagged sentences with subtitles and timestamps
	sentsences_tagged_2 = script_aligner(sentences_tagged, subtitles, timestamps)

	# Create dataframe
	df = pandas.DataFrame(sentsences_tagged_2)
		
	# Write dataframe to CSV file
	df.to_csv(args.output_file, index=False, header=True)

	# Print success message
	print('Script and subtitles have successfully been aligned to {0}'.format(sys.argv[3]))


if __name__ == "__main__":
	main(sys.argv)
