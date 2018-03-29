
# coding: utf-8

# In[21]:


import os
import sys
import operator
import numpy as np

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
		self.SEPERATOR = '****************#################*****************###############\n'
		self.readModelFromFile()
		
	def readModelFromFile(self):
		data = getFileContents('nbmodel.txt')
		self.target_to_index = {}
		self.target_probabilities = [0.0, 0.0, 0.0, 0.0]
		self.word_to_class_probabilities = []
		self.word_to_index = {}
		
		switch = 0
		for line in data:
			if line == self.SEPERATOR:
				switch += 1
				continue
				
			if switch == 0:
				target_name, index, probability = line.strip().split('\t')
				index = int(index)
				self.target_to_index[target_name] = index
				self.target_probabilities[index] = float(probability)
				
			if switch == 1:
				word_probs = map(float, line.strip().split('\t'))
				self.word_to_class_probabilities.append(word_probs)
			
			if switch == 2:
				word, index = line.strip().split('\t')
				index = int(index)
				self.word_to_index[word] = index
				
		
	def negateWords(self, sentence):
		return sentence
		words = sentence.split()
		start_negation = False
		new_words = []
		for word in words:
			if word.lower() in ['not', "don't", "haven't"]:
				start_negation = True
			if start_negation:
				new_words.append('not_' + word)
			else:
				new_words.append(word)
			if word[-1] in [',', '.']:
				start_negation = False
		return ' '.join(new_words)
				
	def give_base_word(self, word):
		# return word
		base_word = word
		if word.endswith('ing'):
			# return word
			base_word = word[:-3]
			if base_word[-1] == base_word[-2]:
				base_word = base_word[:-1]
			elif base_word[-1] == 'e':
				pass
			elif base_word[-1] == 'k' and base_word[-2] == 'c':
				base_word = base_word[:-1]
			elif base_word[-2] in ['e']:
				pass
			else:
				base_word += 'e'
		if word.endswith('ed'):
			base_word = word[:-2]
			if base_word[-1] == base_word[-2]:
				base_word = base_word[:-1]
			elif base_word[-1] == 'y':
				pass
			elif base_word[-1] == 'e':
				pass
			elif base_word[-1] == 'i':
				base_word = base_word[:-1] + 'y'
			elif base_word[-1] == 'k' and base_word[-2] == 'c':
				base_word = base_word[:-1]
			elif base_word[-2] in ['e']:
				pass
			elif base_word[-2] in ['a', 'e', 'i', 'o', 'u'] and base_word[-3]  not in ['a', 'e', 'i', 'o', 'u']:
				# pass
				base_word += 'e'
			else:
				pass
		return base_word
			
	def clean_sentence(self, sentence):
		sentence = self.negateWords(sentence)
		chars_to_remove = ['~', '`','.', '!', '?', "'", '@', '#', '$', '%',\
							'^', '&', ',', '(', ')', '-', '_', '+',\
							'=', '<', '>', ';', ':', '"', '[', ']',\
							'\\', '|', '~', '0', '1', '2', '3', '4',\
							'5', '6', '7', '8', '9']
		sentence = sentence.lower()
		for char in chars_to_remove:
			sentence = sentence.replace(char, ' ')
		words = sentence.split()
		words = [word for word in words if len(word) > 4]
		# words = [ self.give_base_word(word) for word in words ]
		# words = [word if not word.endswith('ed') else word[:-2] for word in words]
		# words = [word if not word.endswith('ing') else word[:-3] for word in words]
		return words
	
	
	def getTargetIndexFromName(self, target_name):
		return self.target_to_index[target_name]
	
	def getSentenceProbabilityWithClass(self, sentence):
		prob_true = self.target_probabilities[0]
		prob_fake = self.target_probabilities[1]
		prob_pos = self.target_probabilities[2]
		prob_neg = self.target_probabilities[3]
		
		sentence_id = sentence.strip().split(' ')[0]
		sentence = self.negateWords(sentence)
		words = self.clean_sentence(sentence)
		for word in words[1:]:
			try:
				word_index = self.word_to_index[word]
			except KeyError as ex:
				continue
			prob_true += self.word_to_class_probabilities[word_index][0]
			prob_fake += self.word_to_class_probabilities[word_index][1]
			prob_pos += self.word_to_class_probabilities[word_index][2]
			prob_neg += self.word_to_class_probabilities[word_index][3]
			
		truthfulness = 'True' if prob_true > prob_fake else 'Fake'
		emotion = 'Pos' if prob_pos > prob_neg else 'Neg'
		
		return '%s %s %s'%(sentence_id, truthfulness, emotion)
	
	def predict(self, untagged_data):
		output = []
		for sentence in untagged_data:
			output.append('%s\n'%(self.getSentenceProbabilityWithClass(sentence)))
		return output


# In[24]:


if __name__ == '__main__':
	model = NaiveBayes()
	untagged_data = getFileFromCommandLine()
	# untagged_data = getFileContents('data/dev-text.txt')
	predicted = model.predict(untagged_data)
	writeOutputToFile(predicted)
	print "Classification Done"
	

