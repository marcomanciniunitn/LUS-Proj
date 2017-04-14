'''
LUS mid-term project, Spring 2017
Student: Marco Mancini, 187403

This was a test to see if the clusters of concepts with more performance dispersions give better performances. 
What is changed with respect to the other versions is the following composition of machines:
1- Word -> Cluster, this transducer basically map words into cluster of concepts (if the word should not be mapped to any cluster than it is mapped to its concept)
2- Cluster -> Concept, this transducer re-map the clusters into concepts (the likelihoods has been calculated as C(Cluster, Concept)/C(Cluster))
3- Language Model for the concepts

These three machines then have been composed and tested, but the performances (FB1 measure particularly) has been dropped of 4/5%, then I've decided not to continue
with this implementation.

'''
from __future__ import print_function
import sys
import math
import os
from subprocess import Popen

global order
global smoothing_algo
global threshold
global wordCutoff
global feature

#Set of smoothing algorithms and orders usable to create the LM
smoothing = ["absolute","katz","kneser_ney","presmoothed","unsmoothed","witten_bell"]

LEXICON_FILE_NAME = 'lexicon.txt'
TRAINING_SET = 'train.txt'
TEST_SET = 'test.txt'
CONCEPT_FILE = "concepts.txt"
TRAINING_CONCEPTS = "training_Concepts.txt"

#This function is used to create the lexicon from the likelihood dictionary, it is useful since
# if the cutoff frequency is requested the lexicon need to be revisited.
def createLexicon(likelihood):
	lexiconFile = open(LEXICON_FILE_NAME, "w")
	indexLex = 0

	lexicon = list()

	for item in likelihood:
		values = item.split( )
		word = values[0]
		concept = values[1]
		if word not in lexicon and word != "<unk>":
			lexicon.append(word)
		if concept not in lexicon:
			lexicon.append(concept)

	lexiconFile.write("<eps>\t" + str(indexLex) + "\n")
	indexLex += 1
	for item in lexicon:
		lexiconFile.write(item + "\t" + str(indexLex) + "\n")
		indexLex += 1
	lexiconFile.write("<unk>\t" + str(indexLex))
	lexiconFile.close()

def appendWordsToLexicon(likelihood):
	lexiconFile = open(LEXICON_FILE_NAME, "r")
	oldItems = list()
	index = 0

	for item in lexiconFile:
		toAdd = item.split("\t")[0]
		if "<unk>" != toAdd:
			oldItems.append(toAdd)

	lexiconFile.close()
	newLex = open(LEXICON_FILE_NAME, "w")

	for it in oldItems:
		newLex.write(it + "\t" + str(index) + "\n")
		index += 1

	for lik in likelihood:
		values = lik.split( )
		tag = values[0]
		conc = values[1]
		if tag not in oldItems:
			oldItems.append(tag)
			newLex.write(tag + "\t" + str(index) + "\n")
			index += 1
		if conc not in oldItems:
			oldItems.append(conc)
			newLex.write(conc + "\t" + str(index) + "\n")
			index += 1
	newLex.write("<unk>\t" + str(index))
	newLex.close()


def addToDictionary(item, dictionary):
	if item in dictionary:
		dictionary[item] += 1
	else:
		dictionary[item] = 1

def sanitizeString(item):
	if item.find('\n') != -1:
		item = item[0 : item.find('\n')]
	return item

#Compute likelihood p(wi | ci) as Counter(ci, wi)/ Counter(ci)
def computeLikelihood(likelihoodCounters, conceptCounter):
	likelihood = dict()
	for likelihoodCounter in likelihoodCounters.keys():
		likelihood[likelihoodCounter] = likelihoodCounters[likelihoodCounter] / float(conceptCounter[likelihoodCounter.split(" ")[1]])
	return likelihood

def computeLikelihood2(likelihoodCounters, conceptCounter):
	likelihood = dict()
	for likelihoodCounter in likelihoodCounters.keys():
		likelihood[likelihoodCounter] = likelihoodCounters[likelihoodCounter] / float(conceptCounter[likelihoodCounter.split(" ")[0]])
	return likelihood



#This kind of cut-off frequency works only on the frequency of the words, this  is the standard cut-off which basically
# subdivide the accumulated counter (accumulated looking for words with less frequency wrt a certain threshold) equally between all the <unk>-concept pairs.
def computeCutOffOnWords(wordToConceptCounter, threshold, concepts, conceptCounter, separator):
	wordCounters = dict()
	toCutOff = list()
	returnConcept = dict()
	cumulativeCounter = 0

	#Retrieve accumulate counters for the words, from the wordToConcept counter
	for item in wordToConceptCounter.keys():
		word = item.split(separator)[0]
		if word not in wordCounters:
			wordCounters[word] = wordToConceptCounter[item]
		else:
			wordCounters[word] += wordToConceptCounter[item]

	#Find the words to be cut off and accumulate the counter
	for w in wordCounters.keys():
		if wordCounters[w] <= threshold:
			toCutOff.append(w)
			cumulativeCounter += wordCounters[w]

	#Populate the word to concept counters without the cutted off words
	for wordToConcept in wordToConceptCounter.keys():
		if wordToConcept.split(separator)[0] not in toCutOff:
			returnConcept[wordToConcept] = wordToConceptCounter[wordToConcept]

	#Add unk  + concept pairs
	for concept in concepts:
		toInsert = "<unk> " + concept
		returnConcept[toInsert] = cumulativeCounter / float(conceptCounter)

	return returnConcept

#This is another kind of cutoff, it does not works only on the word frequency but it take into account the (word-pos/lemma-pos)-concept frequency and cut-off using such guideline.
def computeCutOffOnWordsAndConcept(wordToConceptCounter, threshold, concepts, conceptCounter):
	returnConcept = dict()
	cumulativeCounter = 0
	#Delete the counters under a certain threshold and cumulate them
	# in order to be used for the <unk> - concept pairs
	#All the removed tokens must be removed also from the lexicon
	for counter in wordToConceptCounter.keys():
		if wordToConceptCounter[counter] <= threshold:
			cumulativeCounter += wordToConceptCounter[counter]
		else:
			returnConcept[counter] = wordToConceptCounter[counter]

	for concept in concepts:
		toInsert = "<unk> " + concept
		returnConcept[toInsert] = cumulativeCounter / float(conceptCounter)	

	return returnConcept


#This function permits to smooth the likelihood in order to take care about
#the unknown values, it needs the conceptFileName of the file containing all the concepts with no repetitions
# the last parameters (cutOffFreq) permits to enable the frequency cut off, otherwise the 
# pairs <unk>-concept will have a probability equal to 1/#concepts
#The returned value is the final smoothed likelihood, which will be used to compute the FST 
#The separator is used to separate the words from the PoS and/or lemmas, since the added features are taken jointly to the word.
def smoothLikelihoodAndComputeProbabilities(conceptCounter, likelihoodCounters, threshold, conceptFileName, cutOffFreq, noiseCutOff, separator):
	conceptFile = open(conceptFileName, "r")
	concepts = list()
	conCounter = 0
	cumulativeCounter = 0

	likelihood = dict()

	for concept in conceptFile:
		if concept != "\n":
			concepts.append(sanitizeString(concept))
			conCounter += 1

	conceptFile.close()

	#enable frequency cut off
	if cutOffFreq is True:
		if noiseCutOff:
			likelihoodCounters = computeCutOffOnWordsAndConcept(likelihoodCounters,threshold, concepts, conCounter)
		else:
			likelihoodCounters = computeCutOffOnWords(likelihoodCounters, threshold, concepts, conCounter, separator)
		likelihood = computeLikelihood(likelihoodCounters, conceptCounter)
			
	#No frequency cut-off requested, basically add 1/#concepts to each pair <unk>-concept
	else:
		likelihood = computeLikelihood(likelihoodCounters, conceptCounter)
		#Adding 1/#concept as probability for each pair <unk>-concept
		for concept in concepts:
			toInsert = "<unk> " + concept
			likelihood[toInsert] = 1/float(conCounter)
			
	return likelihood

#This function permits to smooth the likelihood in order to take care about
#the unknown values, it needs the conceptFileName of the file containing all the concepts with no repetitions
# the last parameters (cutOffFreq) permits to enable the frequency cut off, otherwise the 
# pairs <unk>-concept will have a probability equal to 1/#concepts
#The returned value is the final smoothed likelihood, which will be used to compute the FST 
#The separator is used to separate the words from the PoS and/or lemmas, since the added features are taken jointly to the word.
def smoothLikelihoodAndComputeProbabilities2(conceptCounter, likelihoodCounters, threshold, conceptFileName, cutOffFreq, noiseCutOff, separator):
	conceptFile = open(conceptFileName, "r")
	concepts = list()
	conCounter = 0
	cumulativeCounter = 0

	likelihood = dict()

	for concept in conceptFile:
		if concept != "\n":
			concepts.append(sanitizeString(concept))
			conCounter += 1

	conceptFile.close()

	#enable frequency cut off
	if cutOffFreq is True:
		if noiseCutOff:
			likelihoodCounters = computeCutOffOnWordsAndConcept(likelihoodCounters,threshold, concepts, conCounter)
		else:
			likelihoodCounters = computeCutOffOnWords(likelihoodCounters, threshold, concepts, conCounter, separator)
		likelihood = computeLikelihood2(likelihoodCounters, conceptCounter)
			
	#No frequency cut-off requested, basically add 1/#concepts to each pair <unk>-concept
	else:
		likelihood = computeLikelihood2(likelihoodCounters, conceptCounter)
		#Adding 1/#concept as probability for each pair <unk>-concept
		for concept in concepts:
			toInsert = "<unk> " + concept
			likelihood[toInsert] = 1/float(conCounter)
			
	return likelihood


#Compute the basic counters, then thgte smoothing + probability function will be used
# to take care about unknowns and compute probabilities
def computeBasicCounters(trainingFileName, col1, col2):
	trainingFile = open(trainingFileName, "r")
	
	conceptCounter = dict()
	wordToConceptCounter = dict()

	for line in trainingFile:
		values = line.split("\t")
		if len(values) == 3:
			word = sanitizeString(values[col1])
			concept = sanitizeString(values[col2])
			
			#adding priors counter (concepts)
			addToDictionary(concept, conceptCounter)

			#generate likelihood key
			likelihoodKey = word +  " " + concept
			addToDictionary(likelihoodKey, wordToConceptCounter)

	return conceptCounter, wordToConceptCounter

#This function compute the likelihood transducer
def computeLikelihoodFST(likelihood, fstName):
	#File containing the description of the likelihood machine
	fstFileDescr = open("likelihoodFST.descr", "w")
	#Compute the costs
	likelihoodCosts = dict()
	for item in likelihood.keys():
		likelihoodCosts[item] = - math.log(likelihood[item])

	for cost in likelihoodCosts.keys():
		values = cost.split( )
		word = sanitizeString(values[0])
		concept = sanitizeString(values[1])
		fstFileDescr.write("0\t0\t" + word + "\t" + concept + "\t%.5f" % likelihoodCosts[cost] + "\n")

	fstFileDescr.write("0")
	fstFileDescr.close()
	os.system("fstcompile --isymbols=" + LEXICON_FILE_NAME + " --osymbols=" + LEXICON_FILE_NAME + " likelihoodFST.descr | fstarcsort > " + fstName)
	os.system("rm likelihoodFST.descr")

#Generate the Language Model FST, the order parameter is used to change the n-gram size, the smoothing algorithm is used to select which
# smoothing algorithm to use (the initial array indicates all the possible algorithms)
#The training file used is the one generated by the function generateTrainingConcepts present in the util.py file, opengrams need it to compute the n-grams.
def computeLanguageModelFST(trainingFileName, order, smoothingAlgorithm, fstName):
	os.system("farcompilestrings --symbols=" + LEXICON_FILE_NAME + " --keep_symbols=1 --unknown_symbol='<unk>' " + trainingFileName + " | ngramcount --order=" + str(order) + " | ngrammake --method=" + smoothingAlgorithm + " | fstarcsort > " + fstName)

#This function compute the final Trasducer, the one composed from the likelihood FST and the LM trasducer, it will be
# composed with the sentences FSTs in order to get the most probable concepts given a set of words.
def composeFST(fst1, fst2, resultFst):
	os.system("fstcompose " + fst1 + " " + fst2 + " > " + resultFst)

#Given a string it generates the relative FST
def sentenceToFsa(string):
	values = string.split( )

	toExecute = 'echo "'
	for word in values:
		toExecute += str(word +  " ") 
	toExecute += '" | farcompilestrings --symbols=' + LEXICON_FILE_NAME + " --unknown_symbol='<unk>' --generate_keys=1 --keep_symbols | farextract --filename_suffix='.fst' "
	os.system(toExecute)
	os.system('mv 1.fst sentenceFST.fst')

#This function create the file results.txt in the format required by the evaluation tool. 
# This file will be passed to the evaluation tool in order to have all the measurements.
def tagTestSet(testSet):
	testFile = open(testSet, 'r')
	resultFile = open('result.txt', 'w')
	performanceFile = open("results/performances" + smoothing_algo + "_" + order + "_" + threshold + ".txt",  "w")
	reconstructedString = ""
	concepts = ""

	for line in testFile:
		if line != '\n':
			values = line.split('\t')
			reconstructedString += values[0] + ' '
			concepts += values[1] + ' '
		else:
			sentenceToFsa(reconstructedString)
			os.system("fstcompose sentenceFST.fst finalFST.fst | fstshortestpath | fstrmepsilon | fsttopsort |fstprint --isymbols=" + LEXICON_FILE_NAME + " --osymbols=" + LEXICON_FILE_NAME + " > result.fst")
			res = open("result.fst", "r")
			index = 0
			for state in res:
				originalStrings = reconstructedString.split( ) 
				originalConcepts = concepts.split( ) 
				values = state.split( )
				if len(values) == 5:
					resultFile.write(originalStrings[index] + " " + originalConcepts[index] + " " + values[3]  + "\n")
					index += 1
			resultFile.write("\n")
			reconstructedString = ""
			concepts = ""
			res.close()

	testFile.close()
	resultFile.close()

	performanceFile.write("Smoothing = " + smoothing_algo + "  Order = " + order + "  Threshold = " + threshold + " [0: No cut-off]" + " Word-cutoff: " + wordCutoff +"[1: word-cutoff, 0:noise cut-off] \n")
	performanceFile.close()
	process = Popen("./conlleval.pl < result.txt >> results/performances" + smoothing_algo + "_" + order + "_" + threshold + ".txt", shell=True)
	process.communicate()
	print("-Performances calculated!\n-File=results/performances" + smoothing_algo + "_" + order + "_" + threshold + ".txt")
#Used to clean the directory from files used during the computation
def cleanDirectory():
	os.system("rm finalFST.fst && rm likelihoodFST.fst && rm priorFST.fst && rm sentenceFST.fst")

#Input validation
def checkForInputErrors(order, smoothing_algo, threhsold, wordCutoff):


	if smoothing_algo not in smoothing:
		return False
	if threshold != "0" and threshold != "1" and threshold != "2" and threshold != "3" and threshold != "4":
		return False
	if wordCutoff != "0" and wordCutoff != "1":
		return False
	return True

#Incorrect syntax function
def printIncorrectSyntax():
	sys.stdout.write("Incorrect syntax, use the following one.\n-arg1=order [1-3] \n-arg2=smoothing [")
	for algo in smoothing: sys.stdout.write("| " + algo + " |")
	sys.stdout.write("] \n-arg3=threshold for cut-off (0-No cutoff) [0-4]\n-arg4=Word cut-off | Noise cut-off [1 = Word-cutoff, 0 = Noise-cutoff] \n")

#This function basically generate the training file on which the transducers will be computed, this function is parametrized
# to work on all the features we want to take into account, depending on the columns specified (i.e. col1 = 0 (word) col2 = 1 (PoS) | col1 = 2 (lemma), col2 = 1 (PoS) ).
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

#This function is used to generate the test set which will be used for the performances. It is paramatrized in order to work with all the
# features we want to take into account, depending on the columns specified (i.e. col1 = 0 (word) col2 = 1 (PoS) | col1 = 2 (lemma), col2 = 1 (PoS) ).
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

#Function used to generate the training set on which opengram will work in order to generate the WFST for the 
# LM regarding the intermediate tags.
def generateTrainingConcepts(trainingFile):
	trainFile = open(trainingFile, "r")
	trainTagFile = open("training_tags.txt", "w")

	for line in trainFile:
		values = line.split('\t')
		if len(values) == 3:
			trainTagFile.write(values[1])
			trainTagFile.write(" ")
		else:
			trainTagFile.write("\n")

	trainFile.close()
	trainTagFile.close()

#Function used to retrieve the updated tags (after grouping the concepts into clusters). It is usefull to create the <unk>-tag pairs during the smoothing
def generateConceptFile(fileName):
	file = open("train.txt", "r")
	concepts = list()

	toWrite = open("tags.txt" , "w")

	for line in file:
		values = line.split("\t")
		if len(values) >= 2:
			concept = values[1]
			if concept not in concepts:
				concepts.append(concept)


	for item in concepts:
		toWrite.write(item + "\n")

#This function is used in order to add clusters of concepts. 
def addTagsToTrainFile(trainFile, toAdd, conceptCol):
	file = open(trainFile, "r")
	trFile = open("train.txt", "w")

	for line in file:
		values = line.split("\t")
		if len(values)>=2:
		
			if (values[conceptCol][0:values[conceptCol].find("\n")]) in toAdd.keys():
				trFile.write(values[0] + "\t" + toAdd[values[conceptCol][0:values[conceptCol].find("\n")]] + "\t" + values[conceptCol][0:values[conceptCol].find("\n")] + "\n")
			else:
				trFile.write(values[0] +  "\t" + values[conceptCol][0:values[conceptCol].find("\n")] + "\t" + values[conceptCol][0:values[conceptCol].find("\n")] + "\n")
		else:
			trFile.write("\n")

	file.close()
	trFile.close()

#Function used to fuse concepts in cluster.
def fuseConcepts(concepts):
	fused = dict()
	for concept in concepts:
		fused["B-" + concept] = "B-group1"
		fused["I-" + concept] = "I-group1"
		
	return fused

if len(sys.argv) == 5:

	order = sys.argv[1]
	smoothing_algo = sys.argv[2]
	threshold = sys.argv[3]
	wordCutoff = sys.argv[4]

	if checkForInputErrors(order, smoothing_algo, threshold, wordCutoff):
		#Preparing the training set with placeholders...
		lista = {"character.name", "producer.name", "director.name"}
		toAdd = fuseConcepts(lista)
		addTagsToTrainFile("NLSPARQL.train.data", toAdd, 1)
		generateConceptFile("")
		generateTrainingConcepts("train.txt")

		#Generate probabilities and machines for Word to tag and LM for tags (placeholders)
		tagCounter, wordTagCounter = computeBasicCounters("train.txt", 0, 1)
		likelihood = smoothLikelihoodAndComputeProbabilities(tagCounter, wordTagCounter, int(threshold), "tags.txt" , True if int(threshold) > 0 else False, False if int(wordCutoff) == 1 else True, " ")

		createLexicon(likelihood)
		computeLikelihoodFST(likelihood,  "wordToTag.fst")
		#omputeLanguageModelFST("training_tags.txt", order, smoothing_algo, "tagLM.fst")
		#composeFST("wordToTag.fst", "tagLM.fst",  "intermediateFST1.fst")

		#Generate probabilities and machines for tag to concept and related LM
		concCounter, tagConceptCounter = computeBasicCounters("train.txt", 1,2)

		tagCounter2, conctotagCounter = computeBasicCounters("train.txt", 2,1)
		#print(tagCounter2)
		#The settings for this machine are not customizable by the user, since no smoothing is needed.

		likelihood2 = smoothLikelihoodAndComputeProbabilities2(tagCounter2, tagConceptCounter, 0, "concepts.txt", False, False, " ")
		appendWordsToLexicon(likelihood2)
		
		computeLikelihoodFST(likelihood2, "tagToConc.fst")
		composeFST("wordToTag.fst", "tagToConc.fst", "intermediateFST1.fst")
		computeLanguageModelFST("training_Concepts.txt", 2 , "kneser_ney", "conceptLM.fst")
		composeFST("intermediateFST1.fst", "conceptLM.fst", "final.fst")

		#composeFST("intermediateFST1.fst", "intermediateFST2.fst", "finalFST.fst")

		#cleanDirectory()

		tagTestSet("NLSPARQL.test.data")
	else:
		printIncorrectSyntax()
else:
	printIncorrectSyntax()


