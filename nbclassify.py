
# coding: utf-8


import os
import sys
import math
import operator
import numpy as np

from nblearn import clean_sentence
from nblearn import negateWords
from nblearn import SEPERATOR

SMALLEST = -999999999999999999999999999999999

def getFileContents(filename):
	data = None
	with open(filename, 'r') as f:
		data = f.readlines()
	return data

def writeOutputToFile(data):
	with open('nboutput.txt', 'w') as f:
		f.write(''.join(data))
		f.close()

def getFileFromCommandLine():
	filename = sys.argv[1]
	return getFileContents(filename)

class NaiveBayes(object):
	def __init__(self):
		self.readModelFromFile()
		
	def readModelFromFile(self):
		data = getFileContents('nbmodel.txt')
		self.target_to_index = {}
		self.target_probabilities = [0.0, 0.0, 0.0, 0.0]
		self.word_to_class_probabilities = []
		self.word_to_index = {}
		
		switch = 0
		for line in data:
			if line == SEPERATOR:
				switch += 1
				continue
				
			if switch == 0:
				target_name, index, probability = line.strip().split('\t')
				index = int(index)
				self.target_to_index[target_name] = index
				self.target_probabilities[index] = float(probability)
				
			if switch == 1:
				try:
					word_probs = map(float, line.strip().split('\t'))
					self.word_to_class_probabilities.append(word_probs)
				except:
					print "Exception raised in word probabilities"
					self.word_to_class_probabilities.append([SMALLEST, SMALLEST, SMALLEST, SMALLEST])
			
			if switch == 2:
				try:
					word, index = line.strip().split('\t')
					index = int(index)
					self.word_to_index[word] = index
				except:
					print "Exception Raise in word to index"
	
	
	def getTargetIndexFromName(self, target_name):
		return self.target_to_index[target_name]
	
	def getSentenceProbabilityWithClass(self, sentence):
		prob_true = self.target_probabilities[0]
		prob_fake = self.target_probabilities[1]
		prob_pos = self.target_probabilities[2]
		prob_neg = self.target_probabilities[3]
		
		sentence_id = sentence.strip().split()[0]
		words = clean_sentence(sentence)
		for word in words[1:]:
			try:
				word_index = self.word_to_index[word]
			except KeyError as ex:
				continue
			# prob_t = self.word_to_class_probabilities[word_index][0]
			# ptob_f = self.word_to_class_probabilities[word_index][1]
			# prob_p = self.word_to_class_probabilities[word_index][2]
			# prob_n = self.word_to_class_probabilities[word_index][3]

			# if (abs(prob_t - ptob_f)/abs(prob_t + ptob_f)) > 0.000092:
			prob_true += self.word_to_class_probabilities[word_index][0]
			prob_fake += self.word_to_class_probabilities[word_index][1]

			# if (abs(prob_p - prob_n)/abs(prob_p + prob_n)) > 0.000092:
			prob_pos += self.word_to_class_probabilities[word_index][2]
			prob_neg += self.word_to_class_probabilities[word_index][3]
			
		truthfulness = 'True' if prob_true > prob_fake else 'Fake'
		emotion = 'Pos' if prob_pos > prob_neg else 'Neg'
		
		return '%s %s %s'%(sentence_id, truthfulness, emotion)
	
	def predict(self, untagged_data):
		output = []
		for sentence in untagged_data:
			try:
				output.append('%s\n'%(self.getSentenceProbabilityWithClass(sentence)))
			except:
				print "Exception raised in sentence classification"
				output.append('sxiWlyB True Pos\n') # Dummy output in case of a failure
		return output


# In[24]:


if __name__ == '__main__':
	model = NaiveBayes()
	untagged_data = getFileFromCommandLine()
	# untagged_data = getFileContents('data/dev-text.txt')
	predicted = model.predict(untagged_data)
	writeOutputToFile(predicted)
	print "Classification Done"
	

