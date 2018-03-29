import os
import sys
import operator
import numpy as np

def getFileContents(filename):
	data = None
	with open(filename, 'r') as f:
		data = f.readlines()
	return data

def updateMatrix(matrix, category, actual, predicted):
	if actual == predicted and actual == category:
		matrix[0][0] += 1
	elif actual == predicted and actual != category:
		matrix[1][1] += 1
	elif category == predicted and actual != category:
		matrix[0][1] += 1
	elif category == actual and predicted != category:
		matrix[1][0] += 1

def calculatePrecision(matrix):
	return (1.0 * matrix[0][0])/(matrix[0][0] + matrix[0][1])

def calculateRecall(matrix):
	return (1.0 * matrix[0][0])/(matrix[0][0] + matrix[1][0])

def calculateF1(precision, recall):
	return (2.0 * precision * recall)/(precision + recall)

def calculateForClass(class_name, matrix):
	global total_f1
	precision = calculatePrecision(matrix)
	recall = calculateRecall(matrix)
	f1 = calculateF1(precision, recall)
	total_f1 += f1

	output = ('%s'%(class_name)).ljust(15)
	output += ('%.3f'%(precision)).ljust(15)
	output += ('%.3f'%(recall)).ljust(10)
	output += ('%.3f'%(f1)).ljust(10)
	print output

def calculateMetrics(predicted, actual):
	true_mat = [[0, 0], [0, 0]]
	fake_mat = [[0, 0], [0, 0]]
	pos_mat = [[0, 0], [0, 0]]
	neg_mat = [[0, 0], [0, 0]]

	true = [['Pos']]

	for pred, act in zip(predicted, actual):
		pred = pred.strip().split()[1:]
		act = act.strip().split()[1:]
		updateMatrix(neg_mat, 'Neg', act[1], pred[1])
		updateMatrix(true_mat, 'True', act[0], pred[0])
		updateMatrix(pos_mat, 'Pos', act[1], pred[1])
		updateMatrix(fake_mat, 'Fake', act[0], pred[0])
	print '-'*50
	print 'Class Name'.ljust(15) + 'Precision'.ljust(15) \
			+ 'Recall'.ljust(10) + 'F1'.ljust(10)
	print '-'*50

	global total_f1
	total_f1 = 0
	calculateForClass('True', true_mat)
	calculateForClass('Fake', fake_mat)
	calculateForClass('Pos', pos_mat)
	calculateForClass('Neg', neg_mat)

	print "\nMean. F1 : %.3f"% (total_f1/4.0)


def computeAccuracy(predicted, expected):
	total = 0
	correct = 0
	for exp, pred in zip(expected, predicted):
		if exp == pred:
			correct += 1
		total += 1
	print "Accuracy : %.3f %%"%(correct*100.0/total)


if __name__ == '__main__':
	total_f1 = 0
	predicted = getFileContents('nboutput.txt')
	actual = getFileContents('data/dev-key.txt')
	calculateMetrics(predicted, actual)
	computeAccuracy(predicted, actual)
