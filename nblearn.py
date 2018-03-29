
# coding: utf-8

# In[10]:


import os
import sys
import operator
import numpy as np

def getFileContents(filename):
	data = None
	with open(filename, 'r') as f:
		data = f.readlines()
	return data

def getFileFromCommandLine():
	filename = sys.argv[1]
	return getFileContents(filename)

class NaiveBayes(object):
	def __init__(self, data):
		self.raw_data = data
		self.word_to_index = {}
		self.target_to_index = {'True': 0, 'Fake': 1, 'Pos': 2, 'Neg': 3}
		self.word_to_class_map = []
		self.total_words = 0
		self.index_to_word = {}
		self.index_to_target = {}
		self.target_counts = [0, 0, 0, 0]
		self.word_to_class_probabilities = None
		self.target_probabilities = None
		self.SEPERATOR = '****************#################*****************###############\n'
		
	def writeModelToFile(self):
		output = ''
		
		# Writes target names with index and their probabilities
		for target_name, index in sorted(self.target_to_index.items(), key=operator.itemgetter(1)):
			output += '%s\t%d\t%f\n'%(target_name, index, self.target_probabilities[index])
		
		output += self.SEPERATOR
		
		# Writes word target probabilities
		for i in range(len(self.word_to_class_probabilities)):
			output += '\t'.join(map(str, self.word_to_class_probabilities[i])) + '\n'
			
		output += self.SEPERATOR
		
		# Writes all words with their indexes
		for word, index in sorted(self.word_to_index.items(), key=operator.itemgetter(1)):
			output += '%s\t%d\n'%(word, index)
			
		output += self.SEPERATOR
		
		with open('nbmodel.txt', 'w') as f:
			f.write(output)
			f.close()
		
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
			print word.ljust(15), ' => ', base_word.ljust(15)

		return base_word

			
	def clean_sentence(self, sentence):
		sentence = self.negateWords(sentence)
		chars_to_remove = ['~', '`','.', '!', '?', "'", '@', '#', '$', '%',\
							'^', '&', ',', '(', ')', '-', '_', '+',\
							'=', '<', '>', ';', ':', '"', '[', ']',\
							'\\', '|', '~', '0', '1', '2', '3', '4',\
							'5', '6', '7', '8', '9']

		stop_words =  ['a','about','above','after','again','against','all','am','an','and','any','are','as','at','be',\
				'because','been','before','being','below','between','both','but','by','could','did','do','does',\
				'doing','down','during','each','few','for','from','further','had','has','have','having','he',\
				'd','ll','s','her','here','hers','herself','him','himself','his','how','i','m','ve','if','in',\
				'into','is','it','its','itself','let','me','more','most','my','myself','nor','of','on','once',\
				'only','or','other','ought','our','ours','ourselves','out','over','own','same','she','should',\
				'so','some','such','than','that','the','their','theirs','them','themselves','then','there',\
				'these','they','re','this','those','through','to','too','under','until','up','very','was',
				'we','were','what','when','where','which','while','who','whom','why','with','would',\
				'you','your','yours','yourself','yourselves']
				  
		sentence = sentence.lower()
		for char in chars_to_remove:
			sentence = sentence.replace(char, ' ')

		# for stop_word in stop_words:
		#     sentence = sentence.replace(stop_word, ' ')

		words = sentence.split()
		words = [word for word in words if len(word) > 4]
		# words = [ self.give_base_word(word) for word in words ]
		# words = [word if not word.endswith('ed') else word[:-2] for word in words]
		# words = [word if not word.endswith('ing') else word[:-3] for word in words]
		return words
	
	def splitClassNData(self, line):
		tokens = line.strip().split(' ')
		data_id = tokens[0]
		truthfulness = tokens[1]
		emotion = tokens[2]
		data = ' '.join(tokens[3:])
		data = self.clean_sentence(data)
		return (data_id, truthfulness, emotion, data)
	
	def reverseMapping(self):
		for word, index in self.word_to_index.iteritems():
			self.index_to_word[index] = word
		for target_name, index in self.target_to_index.iteritems():
			self.index_to_target[index] = target_name
	
	
	def addWordsToClass(self, target_names, words):
		for word in words:
			try:
				word_index = self.word_to_index[word]
			except KeyError as ex:
				#New word is encountered
				word_index = self.total_words
				self.word_to_index[word] = word_index
				self.word_to_class_map.append([0, 0, 0, 0])
				self.total_words += 1
				
			for target_name in target_names:
				self.word_to_class_map[word_index][self.getTargetIndexFromName(target_name)] += 1
		
	def getTargetIndexFromName(self, target_name):
		return self.target_to_index[target_name]
		
	def smoothObservations(self):
		self.word_to_class_map = self.word_to_class_map + 1
	
	def calculateProbabilities(self):
		self.word_to_class_probabilities = (self.word_to_class_map*1.0)/self.word_to_class_map.sum(axis=0, keepdims=True)
		self.word_to_class_probabilities = np.log(self.word_to_class_probabilities)
		self.target_probabilities = np.array(self.target_counts, dtype=np.float64) / len(self.raw_data)
		self.target_probabilities = np.log(self.target_probabilities)
	
	def incrementTargetCounts(self, target_name):
		self.target_counts[self.target_to_index[target_name]] += 1
		
	def fit(self):
		for line in self.raw_data:
			data_id, truthfulness, emotion, words = self.splitClassNData(line)
			self.addWordsToClass([truthfulness, emotion], words)
			self.incrementTargetCounts(truthfulness)
			self.incrementTargetCounts(emotion)
			
		self.reverseMapping()
		self.word_to_class_map = np.array(self.word_to_class_map, dtype=np.float64)
		self.smoothObservations()
		self.calculateProbabilities()
# In[11]:


if __name__ == '__main__':
	tagged_data = getFileFromCommandLine()
	# tagged_data = getFileContents('data/train-labeled.txt')
	model = NaiveBayes(tagged_data)
	model.fit()
	model.writeModelToFile()
	print "Traning Done"

