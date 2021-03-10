import sys


def main(argv):
	with open('mi.txt', 'r') as script:
		lines = script.readlines()
		#no_newline = remove_newline(lines)
		#print(no_newline)
		for line in lines:
			if line == '\n':
				lines.remove(line)
		print(''.join(lines))

if __name__ == '__main__':
	main(sys.argv)