import spacy
import pronouncing
import pyphen
import random
from datetime import datetime

print('Loading...')
random.seed(datetime.now())
response = 'y'

import sys
sys.setrecursionlimit(5000)

# generate a list of random words from a word list
def generateWords(wlist, num, pos='DEFAUlT'):
	words = wlist
	word_list = []
	i = 0
	while i < num:
		word = random.choice(words)
		if pos is 'DEFAULT':
			word_list.append(word)
		else:
			pos_check = nlp(word)
			for token in pos_check:
				if token.pos_ is not pos:
					i -= 1
				else:
					word_list.append(word)
		i += 1
	return word_list

# use spacey to find most similar word in a list, use recursion to reach threshold
def getMostSimilar(word, wlist, thresh=0):
	similarities = []
	token1 = nlp(word)
	for w in wlist:
		token2 = nlp(w)
		for t1 in token1:
			for t2 in token2:
				similarities.append(t1.similarity(t2))
	if max(similarities) < thresh:
		return 'NULL'
		# return getMostSimilar(word, wlist, thresh)
	return wlist[similarities.index(max(similarities))]

# use pronouncingpy to find number of syllables in a line
# def countSyllables(line):
# 	count = 0
# 	for word in line.split():
# 		word = ''.join([i for i in word if i.isalpha()]) # remove punctuations
# 		pronunciation_list = pronouncing.phones_for_word(word)
# 		count += pronouncing.syllable_count(pronunciation_list[0])
# 		pronunciation_list = []
# 	return count

# use pyphen to find number of syllables
def countSyllables(line):
	count = 0
	dic = pyphen.Pyphen(lang='en')
	for word in line.split():
		str2 = dic.inserted(word).split('-')
		count += len(str2)
	return count

# load word list and spacy model
all_words = []
f = open('dictionary/popular.txt', 'r')
for word in f:
	all_words.append(word.strip('\n'))
nlp = spacy.load('en_core_web_lg')

while response is 'y':

	random.seed(datetime.now())

	word_dict = {
		'word': '',
		'lemma': '',
		'pos': '',
		'tag': ''
	}

	words_nlp = []

	count_syllables = True

	###
	# Haiku
	# 5 syllables
	# 7 syllables
	# 5 syllables

	# get first line from user
	first_line = input('This is a Haiku bot! Please write the first line:\n')
	second_line = ''
	third_line = ''
	while True:
		if countSyllables(first_line) is 5:
			break
		else:
			first_line = input('The first line needs to have 5 syllables! Please enter your line again:\n')

	# analyze first line
	doc = nlp(first_line)
	for token in doc:
		word_dict['word'] = token.text
		word_dict['lemma'] = token.lemma_
		word_dict['pos'] = token.pos_
		word_dict['tag'] = token.tag_
		words_nlp.append(word_dict)
		word_dict = {}

	for word in words_nlp:

		# usually the most important word in a line is the noun, if no noun, choose last word
		if word['pos'] is 'NOUN' or word is words_nlp[-1]:
			theme = word['lemma']

			# find a noun similar to the most important word
			noun2 = 'NULL'
			while noun2 is 'NULL':
				noun2 = getMostSimilar(word['word'], generateWords(all_words, 20, 'NOUN'), thresh=0.35)
			print(noun2)
			break

	### Writing Second Line

	while countSyllables(second_line) is not 7:

		second_line_words = [noun2]

		# randomly generates 1-3 similar words
		for x in range(random.randint(1, 3)):
			if x is 1:
				new_verb = 'NULL'
				while new_verb is 'NULL':
					new_verb = getMostSimilar(noun2, generateWords(all_words, 10, 'VERB'), thresh=0.15)
				print(new_verb)
				second_line_words.append(new_verb)
			else:
				new_word = 'NULL'
				while new_word is 'NULL':
					new_word = getMostSimilar(noun2, generateWords(all_words, 10, 'DEFAULT'), thresh=0.15)
				print(new_word)
				second_line_words.append(new_word)

		# generate a random adjective
		random_adj = generateWords(all_words, 1, 'ADJ')[0]
		second_line_words.append(random_adj)

		# shuffle order of the words
		random.shuffle(second_line_words)

		second_line = ' '.join(second_line_words)
		print(second_line)

	### Writing Third Line

	# generate a random preposition
	prep = generateWords(all_words, 1, 'ADP')[0]

	while countSyllables(third_line) is not 5:

		third_line_words = [prep]

		if random.randint(0, 99) % 3 is not 0:
			new_word = 'NULL'
			while new_word is 'NULL':
				new_word = getMostSimilar(theme, generateWords(all_words, 20, 'DEFAULT'), thresh=0.30)
			print(new_word)
			third_line_words.append(new_word)
		else:
			new_adv = 'NULL'
			while new_adv is 'NULL':
				new_adv = getMostSimilar(theme, generateWords(all_words, 10, 'ADV'), thresh=0.10)
			print(new_adv)
			third_line_words.append(new_adv)

			new_adj = 'NULL'
			while new_adj is 'NULL':
				new_adj = getMostSimilar(theme, generateWords(all_words, 20, 'ADJ'), thresh=0.20)
			print(new_adj)
			third_line_words.append(new_adj)


		if random.randint(0, 99) % 3 is 0:
			third_line_words.append(theme)
		else:
			noun3 = 'NULL'
			while noun3 is 'NULL':
				noun3 = getMostSimilar(word['word'], generateWords(all_words, 20, 'NOUN'), thresh=0.45)
			third_line_words.append(noun3)


		third_line = ' '.join(third_line_words)
		print(third_line)

	with open(r'haiku.txt', 'r') as f_read:
		l = f_read.readlines()
		haiku_count = int(l[-5].strip())
	with open(r'haiku.txt', 'a') as f_write:
		f_write.writelines([str(haiku_count+1), '\n', first_line, '\n', second_line, '\n', third_line, '\n\n'])

	### Show All Lines
	print('---------------------------')
	print('Here is our haiku:')
	print(first_line)
	print(second_line)
	print(third_line)
	print()
	print('this is also saved in haiku.txt')
	print('---------------------------')
	
	response = input('Continue? y or n: ')














