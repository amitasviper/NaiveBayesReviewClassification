
# coding: utf-8

# In[10]:


import os
import sys
import operator
import numpy as np

SEPERATOR = '****************#################*****************###############\n'

def getFileContents(filename):
	data = None
	with open(filename, 'r') as f:
		data = f.readlines()
	return data

def getFileFromCommandLine():
	filename = sys.argv[1]
	return getFileContents(filename)

def clean_sentence(sentence):
	# sentence = negateWords(sentence)
	chars_to_remove = ['~', '`','.', '!', '?', "'", '@', '#', '$', '%',\
						'^', '&', ',', '(', ')', '-', '_', '+', '*',\
						'=', '<', '>', ';', ':', '"', '[', ']', '/',\
						'\\', '|', '~', '{', '}']

	chars_to_remove += ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

	stop_words =  ['being', 'our', 'd', 'them', 'more', 've', 'd', 'its',\
				    's', 'my', 'such', 'from', 'only', 'as', 'should', 'all',\
				    'over', 'during', 'yourselves', 'has', 'myself', 'am',\
				    'the', 'ourselves', 'did', 'some', 'after', 'that', 'or',\
				    'which', 'if', 'this', 'into', 'having', 'aren', 'could',\
				    'an', 'would', 'it', 'out', 'won', 're', 'themselves',\
				    'whom', 'they', 'couldn', 'is', 'own', 'but', 'up', 'her',\
				    'on', 'while', 'before', 'are', 'both', 'each', 'very',\
				    'he', 'don', 'at', 'had', 'm', 'how', 'wasn', 'was',\
				    'herself', 'nor', 'were', 'yours', 'does', 'down', 'himself',\
				    'ought', 'with', 'ours', 'doing', 'in', 'once', 'him',\
				    'same', 'a', 'isn', 'until', 'who', 'you', 'be', 'between',\
				    'here', 'been', 'll', 'most', 'itself', 'against', 'under',\
				    'so', 'again', 'to', 'when', 'then', 'these', 'of', 'have',\
				    'above', 'by', 'why', 'i', 'theirs', 'yourself', 'for',\
				    'me', 'those', 'further', 'where', 'let', 'below', 'through',\
				    'other', 'than', 'their', 'she', 'your', 'too', 'do', 'and',\
				    'hers', 'we', 'there', 'any', 'because', 'about', 'what', 'few',\
				    'his', 't', 'didn']

	stop_words += ['ourselves','hers','between','yourself','but','again','there','about','once','during','out','very','having','with','they','own','an','be','some','for','do','its','yours','such','into','of','most','itself','other','off','is','s','am','or','who','as','from','him','each','the','themselves','until','below','are','we','these','your','his','through','don','nor','me','were','her','more','himself','this','down','should','our','their','while','above','both','up','to','ours','had','she','all','no','when','at','any','before','them','same','and','been','have','in','will','on','does','yourselves','then','that','because','what','over','why','so','can','did','not','now','under','he','you','herself','has','just','where','too','only','myself','which','those','i','after','few','whom','t','being','if','theirs','my','against','a','by','doing','it','how','further','was','here','tha']
	stop_words = list(set(stop_words))  
	sentence = sentence.lower()

	for char in chars_to_remove:
		sentence = sentence.replace(char, ' ')

	words = sentence.split()

	words = [word for word in words if word not in stop_words]

	# print '\n\n'
	# print sentence
	# # words = sentence.split()
	# print words
	# print '\n\n\n'
	words = [ give_base_word(word) for word in words ]
	# words = [word for word in words if len(word) > 2]
	words = [ word for word in words if len(word.strip()) > 0]

	# words = [word[:-2] if (word.endswith('ed')) and (len(word) > 2) else word for word in words]
	# words = [word if not word.endswith('ing') else word[:-3] for word in words]
	# words = list(set(words))
	# print words
	return words

def give_base_word(word):
	# return word
	base_word = word
	if word.endswith('ing'):
		# return word
		base_word = word[:-3]
		if len(base_word) > 3:
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

	# elif word.endswith('ly') and len(word) > 10:
	# 	base_word = word[:-2]

	elif word.endswith('ed'):
		base_word = word[:-2]
		if len(base_word) < 2:
			base_word = word
		elif base_word[-1] == 'y':
			pass
		elif base_word[-1] == 'e':
			pass
		elif base_word[-1] == 'i':
			base_word = base_word[:-1] + 'y'

		elif len(base_word) > 2 and  base_word[-1] == base_word[-2]:
			base_word = base_word[:-1]
		elif len(base_word) > 2 and  base_word[-1] == 'k' and base_word[-2] == 'c':
			base_word = base_word[:-1]
		elif len(base_word) > 2 and  base_word[-2] in ['e']:
			pass
		elif len(base_word) > 2 and  base_word[-2] in ['a', 'e', 'i', 'o', 'u']:
			# pass
			base_word += 'e'
		else:
			pass

	return base_word

def negateWords(sentence):
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

class NaiveBayes(object):
	def __init__(self, data):
		self.raw_data = data
		self.word_to_index = {}
		self.target_to_index = {'True': 0, 'Fake': 1, 'Pos': 2, 'Neg': 3}
		self.word_to_class_map = []
		self.total_words = 0
		self.target_counts = [0.0, 0.0, 0.0, 0.0]
		self.word_to_class_probabilities = None
		self.target_probabilities = None
		
	def writeModelToFile(self):
		output = ''
		
		# Writes target names with index and their probabilities
		for target_name, index in sorted(self.target_to_index.items(), key=operator.itemgetter(1)):
			output += '%s\t%d\t%f\n'%(target_name, index, self.target_probabilities[index])
		
		output += SEPERATOR
		
		# Writes word target probabilities
		for i in range(len(self.word_to_class_probabilities)):
			output += '\t'.join(map(str, self.word_to_class_probabilities[i])) + '\n'
			
		output += SEPERATOR
		
		# mywords = ''
		# Writes all words with their indexes
		for word, index in sorted(self.word_to_index.items(), key=operator.itemgetter(1)):
			output += '%s\t%d\n'%(word, index)
			# mywords += "'%s',"%(word)
			
		output += SEPERATOR
		
		with open('nbmodel.txt', 'w') as f:
			f.write(output)
			f.close()

		# with open('mywords.txt', 'w') as f:
		# 	f.write(mywords)
		# 	f.close()

	
	def splitClassNData(self, line):
		tokens = line.strip().split()
		data_id = tokens[0]
		truthfulness = tokens[1]
		emotion = tokens[2]
		data = ' '.join(tokens[3:])
		data = clean_sentence(data)
		return (data_id, truthfulness, emotion, data)
	
	
	def addWordsToClass(self, target_names, words):
		for word in words:
			try:
				word_index = self.word_to_index[word]
			except KeyError as ex:
				#New word is encountered
				word_index = self.total_words
				self.word_to_index[word] = word_index
				self.word_to_class_map.append([0.0, 0.0, 0.0, 0.0])
				self.total_words += 1
				
			for target_name in target_names:
				self.word_to_class_map[word_index][self.getTargetIndexFromName(target_name)] += 1
		
	def getTargetIndexFromName(self, target_name):
		return self.target_to_index[target_name]
		
	def smoothObservations(self):
		self.word_to_class_map = self.word_to_class_map + 1
	
	def calculateProbabilities(self):
		self.word_to_class_map = np.array(self.word_to_class_map, dtype=np.float64)
		self.smoothObservations()
		self.word_to_class_probabilities = (self.word_to_class_map*1.0)/self.word_to_class_map.sum(axis=0, keepdims=True)
		self.target_probabilities = np.array(self.target_counts, dtype=np.float64) / len(self.raw_data)
		self.word_to_class_probabilities = np.log(self.word_to_class_probabilities)
		self.target_probabilities = np.log(self.target_probabilities)
	
	def incrementTargetCounts(self, target_name):
		self.target_counts[self.target_to_index[target_name]] += 1
		
	def fit(self):
		for line in self.raw_data:
			try:
				data_id, truthfulness, emotion, words = self.splitClassNData(line)
				self.addWordsToClass([truthfulness, emotion], words)
				self.incrementTargetCounts(truthfulness)
				self.incrementTargetCounts(emotion)
			except:
				print "Exception raised"
			
		self.calculateProbabilities()


if __name__ == '__main__':
	tagged_data = getFileFromCommandLine()
	# tagged_data = getFileContents('data/train-labeled.txt')
	model = NaiveBayes(tagged_data)
	model.fit()
	model.writeModelToFile()
	print "Traning Done"

