import sys
import operator

words = dict()
PoS = dict()
lemmas = dict()
labels = dict()

def changeTrainNOIOB(trainSet):
	trainFile = open(trainSet, "r")
	trainFileFinal = open("train_analysis.txt", "w")

	for line in trainFile:
		values = line.split("\t")
		if len(values) == 4:
			concept = values[3]
			if "O" not in concept:
				concept = concept[2:concept.find("\n")]
			else:
				concept = concept[0:concept.find("\n")]
			trainFileFinal.write(values[0] + "\t" + values[1] + "\t" + values[2] + "\t" + concept + "\n")
		else:
			trainFileFinal.write("\n")

	trainFile.close()
	trainFileFinal.close()

def addToDictionary(item, dictionary):
	if item in dictionary:
		dictionary[item] += 1
	else:
		dictionary[item] = 1

def computeRatio(dictionary, file, column):
	dataFile = open(file, "r")
	totCounter = 0

	res = dict()

	for line in dataFile:
		values = line.split( )
		if len(values) == 4:
			addToDictionary(values[column], dictionary)
			totCounter += 1

	for item in dictionary.keys():
		res[item] = dictionary[item] / float(totCounter)

	sorted_res = sorted(res.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_res

def computeCounter(dictionary, file, column):
	dataFile = open(file, "r")
	totCounter = 0


	for line in dataFile:
		values = line.split( )
		if len(values) == 4:
			addToDictionary(values[column], dictionary)
			totCounter += 1


	sorted_res = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_res

def printResults(resList, file):
	toWrite = open(file, "w")
	#toWrite.write("ANALYZED\tRATIO\n")
	for item in resList:
		toWrite.write(item[0] + "," + str(item[1]))
		toWrite.write("\n")



#changeTrainNOIOB("train_tmp.txt")
res_w = computeRatio(words, "train_analysis.txt", 0)
res_PoS = computeRatio(PoS, "train_analysis.txt", 1)
res_Lemma = computeRatio(lemmas, "train_analysis.txt", 2)
res_Labels = computeRatio(labels, "train_analysis.txt", 3)

printResults(res_w, "words_distrib.txt")
printResults(res_PoS, "PoS_distrib.txt")
printResults(res_Lemma, "lemma_distrib.txt")
printResults(res_Labels, "labels_distrib.txt")


res_w_c = computeCounter(words, "train_analysis.txt", 0)
printResults(res_w_c, "word_counters.txt")