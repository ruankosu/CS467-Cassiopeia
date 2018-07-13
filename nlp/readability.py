#!/usr/bin/python

import string
import re #regular expression library
import sys
import operator
import functools


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
        word.strip('.,!?-*();:\'\"[]{}\\')
        # finds word length
        length = len(word)
        # very correct length and alpha only
        if length > 0 and length < 4:
            if(word.isalpha()):
                return True
        else:
            return False

def count_miniwords(text):
        # map(is_miniword) update count
        miniword_count = len(filter(is_miniword, text.split()))
        return miniword_count

def count_syllables(text):
        # count number of syllables
        return

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
	#4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43
	num_chars = count_chars(text)
	num_words = count_words(text)
	num_sentences = count_sentences(text)
	fki_score = 4.71 * num_chars / num_words + 0.5 * num_words / num_sentences - 21.43
	return fki_score

# Calculates the McAlpine EFLAW Index (designed for ESL learners)
def cal_mei(text):
	#4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43
	num_chars = count_chars(text)
	num_words = count_words(text)
	num_sentences = count_sentences(text)
	mei_score = 4.71 * num_chars / num_words + 0.5 * num_words / num_sentences - 21.43
	return mei_score

# Main
if __name__ == "__main__":
        f = open (sys.argv[1], "r")
        if f.mode == 'r':
               text = f.read()
        #print(cal_ari(text))


