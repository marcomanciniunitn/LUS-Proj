from subprocess import Popen
import random

#Seed used to randomize the sentences for the folds
SEED = 510

folds = dict()

#Function used to retrieve all the sentences 
def retrieveSentences(trainFile):
	testSet = open(trainFile, "r")

	sentences = list()
	accumulate = ""

	for line in testSet:
		if line != "\n":
			accumulate += line 
		else:
			sentences.append(accumulate)
			accumulate = ""

	random.seed(SEED)
	random.shuffle(sentences)

	testSet.close()
	return sentences

#Function used to change all the O concepts of the words into the words themselves
def changeAllO(file, out):
	w = open(out, "w")

	for line in (open(file).readlines()):
		v = line.split("\t")
		if(len(v)>1):
			if v[1][0:1] == "I" or v[1][0:1] == "B":
				w.write(line)
			else:
				w.write(v[0] + "\t" + "$-"+str(v[0])+"\n")
		else:
			w.write("\n")
			flag = 0

	w.close()

#This function populates the folds
def generateFolds(k, sentences):
	tmp = list()

	num_sent = len(sentences) / k
	index = 0
	#creating folds
	for i in range(0,k):

		for el in range(0,num_sent):
			tmp.append(sentences[index])
			index += 1
		folds[i] = tmp
		tmp = list()


#Run the k-cross validation, at each iteration 1 fold is used as test set and the remainings k-1 as test set.
def runValidation(k, order, smoothing):
	print("K-Cross Validation started\n")
	for i in range(0,k):
		print("Iteration #:" + str(i))
		trainF = open("TRAIN.txt", "w")
		testF = open("TEST.txt", "w")

		for fold in folds.keys():
			#test fold, generate test file
			if fold == i:
				for sentence in folds[fold]:
					testF.write(sentence)
					testF.write("\n")
			#train folds, generate train file
			else:
				for sentence in folds[fold]:
					trainF.write(sentence)
					trainF.write("\n")

		trainF.close()
		testF.close()
		#Enhance train set using words instead of concepts for O-concept words.
		changeAllO("TRAIN.txt", "TRAIN_ENHANCED.txt")
		process = Popen("python main.py %s %s %s %s %s" % (order, smoothing, 0, 0, "TEST.txt"), shell=True)
		process.communicate()

sen = retrieveSentences("NLSPARQL.train.data")
generateFolds(10, sen)
runValidation(10, 4, "kneser_ney")


