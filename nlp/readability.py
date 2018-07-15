#!/usr/bin/python

import string
import re #regular expression library
import sys
import operator
import functools
import nltk
import curses
from curses.ascii import isdigit
from nltk.corpus import cmudict
#nltk.download('cmudict')
d = cmudict.dict()


def count_chars(text):
	# count number of letters and numbers
	letters = string.ascii_letters
	digits = string.digits
	letter_count = len(filter(functools.partial(operator.contains, letters), text))
	digit_count = len(filter(functools.partial(operator.contains, digits), text))
	char_count = letter_count + digit_count
	return char_count

def count_words(text):
	# count spaces
	spaces = string.whitespace
	space_count = len(filter(functools.partial(operator.contains, spaces), text))
	return space_count

def is_miniword(word):
        # strip leading and trailing punctuation/non-alpha chars
        word = word.strip('.,!?-*();:\'\"[]{}\\')
        # finds word length
        length = len(word)
        # very correct length and alpha only
        if length > 0 and length < 4:
            if word.isalpha():
                return True
        else:
            return False

def count_miniwords(text):
        # map(is_miniword) update count
        miniword_count = len(filter(is_miniword, text.split()))
        return miniword_count

def count_syllables(text):
        # count number of syllables
        wordlist = text.split()
        syllable_count = 0
        for word in wordlist:
            word = word.strip('.,!?-*();:\'\"[]{}\\')
            # checks if word is alpha && in the dictionary (prevents key errors)
            if word.isalpha() and word in d:
                syllable_count += [len(list(y for y in x if isdigit(y[-1]))) for x in d[word.lower()]][0]
        return syllable_count

def count_sentences(text):
	# count sentences
	sentenceEnd = '.!?'
	sentence_count = len(filter(functools.partial(operator.contains, sentenceEnd), text))
	return sentence_count

# Calculates the Automated Readability Index
def cal_ari(text):
	#4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43
	num_chars = count_chars(text)
	num_words = count_words(text)
	num_sentences = count_sentences(text)
	ari_score = 4.71 * num_chars / num_words + 0.5 * num_words / num_sentences - 21.43
	return ari_score

# Calculates the Flesch-Kincaid Index
def cal_fki(text):
	# 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
	num_words = count_words(text)
	num_sentences = count_sentences(text)
        num_syllables = count_syllables(text)
	fki_score = 206.835 = 1.015 * num_words / num_sentences - 84.6 * num_syllables / num_words
	return fki_score

# Calculates the McAlpine EFLAW Index (designed for ESL learners)
def cal_mei(text):
	#words + miniwords / sentences
	num_words = count_words(text)
	num_miniwords = count_miniwords(text)
        num_sentences = count_sentences(text)
	mei_score = num_words + num_miniwords / num_sentences
	return mei_score

# Main
if __name__ == "__main__":
        f = open (sys.argv[1], "r")
        if f.mode == 'r':
               text = f.read()
        print(cal_ari(text))
        #print(cal_fki(text))
        #print(cal_mei(text))


