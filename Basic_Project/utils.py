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

	trainFile.close()
	trainTagFile.close()

#generateConceptFile("NLSPARQL.train.data")
generateTrainingConcepts("NLSPARQL.train.data")


