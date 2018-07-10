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

def count_sentences(text):
	# count sentence
	sentenceEnd = '.!?'
	sentence_count = len(filter(functools.partial(operator.contains, sentenceEnd), text))
	return sentence_count


def cal_diff(text):
	#4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43
	num_chars = count_chars(text)
	num_words = count_words(text)
	num_sentences = count_sentences(text)
	diff_score = 4.71 * num_chars / num_words + 0.5 * num_words / num_sentences - 21.43
	return diff_score


if __name__ == "__main__":
	f = open (sys.argv[1], "r")
	if f.mode == 'r':
		text = f.read()
	print(cal_diff(text))


