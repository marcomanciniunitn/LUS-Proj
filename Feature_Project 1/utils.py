import sys

#This function has been used to generate the set of concepts 
# it was useful to smooth the likelihood and the relative counters, since here was needed
# the full set of concepts
def generateConceptFile(fileName):
	file = open("NLSPARQL.train.data", "r")
	concepts = list()

	toWrite = open("concepts.txt" , "w")

	for line in file:
		values = line.split("\t")
		if len(values) == 2:
			concept = values[1]
			if concept not in concepts:
				concepts.append(concept)


	for item in concepts:
		toWrite.write(item + "\n")

#This function has been used in the generation of the LM machine,
# since to generate the LM openGram needs it (for the computation of the n-grams)
def generateTrainingConcepts(trainingFile):
	trainFile = open(trainingFile, "r")
	trainTagFile = open("training_Concepts.txt", "w")

	for line in trainFile:
		values = line.split('\t')
		if len(values) == 2:
			trainTagFile.write(values[1][0:values[1].find('\n')])
			trainTagFile.write(" ")
		else:
			trainTagFile.write("\n")

	trainFile.close()
	trainTagFile.close()

def generateTrainingSets(trainingFile, col1, col2):
	trainFile = open(trainingFile, "r")
	trainWordPosFile = open("train.txt", "w")

	for line in trainFile:
		values = line.split("\t")
		if len(values) == 4:
			w1 = values[col1]
			w2 = values[col2]
			concept = values[3][0 : values[3].find("\n")]
			trainWordPosFile.write(w1 + "#" + w2 + "\t" + concept + "\n")
		else:
			trainWordPosFile.write("\n")
	trainFile.close()
	trainWordPosFile.close()

def generateTestSet(testSet, col1, col2):
	testFile = open(testSet, "r");
	finalTesf = open("test.txt", "w")

	for line in testFile:
		values = line.split("\t")
		if len(values) == 4:
			w1 = values[col1]
			w2 = values[col2]
			concept = values[3][0 : values[3].find("\n")]
			finalTesf.write(w1 + "#" + w2 + "\t" + concept + "\n")
		else:
			finalTesf.write("\n")

	testFile.close()
	finalTesf.close()

#generateConceptFile("NLSPARQL.train.data")
generateTrainingConcepts("NLSPARQL.train.data")
#generateTrainingSets("train_tmp.txt", 0,1)
#generateTestSet("test_tmp.txt", 0,1)
