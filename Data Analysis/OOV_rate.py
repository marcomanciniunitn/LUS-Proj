

def calculateOOV(trainFile, testFile):
	fileTr = open(trainFile, "r")
	fileTe = open(testFile, "r")
	inLex = set()
	inTest = set()
	oovSet = set()
	ya = 0
	for line in fileTr:
		values = line.split("\t")
		if len(values) >= 2:

			if values[0] not in inLex:
				#print values[0]
				inLex.add(values[0])

	for lineTe in fileTe:
		val = lineTe.split("\t")
		ya += 1
		if len(val) >= 2:
			if val[0] not in inTest:

				inTest.add(val[0])

	#print inLex
	oovSet = inTest - inLex

	print "-OOV Words-"
	for item in oovSet:
		print item

	print "%: " + str(len(oovSet)/float(len(inTest)))
	print str(len(inTest))

calculateOOV("NLSPARQL.train.data", "NLSPARQL.test.data")

