import spacy
import sys
from textstat.textstat import textstatistics, easy_word_set, legacy_round

def analyze(argv):
	print word_count(argv)
	pass

if __name__ == "__main__":
	text = " ".join(str(x) for x in sys.argv)
	analyze(text)
# if files to analyze are provided in command line
#if len(sys.argv) > 0:
	# for each argument, open the file and analyze its difficuty
#	for f in sys.argv:
		
	

def break_sentences(text):
	nlp = spacy.load('en')
	doc = nlp(text)
	return doc.sents

def word_count(text):
	sentences = break_sentences(text)
	words = 0
	for sentence in sentences:
		words += len([token for token in sentence])
	return words
