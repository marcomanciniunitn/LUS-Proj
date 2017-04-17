import sys
from collections import Counter	
import operator

#This function has been used in order to find, for each word preceeding each B-concept, the ratio of such a word behind such a concept over the whole appearances
# of such a word. It has been useful in order to find the best words to exploit in order to add prior
def findInsights(file, out, toLookFor):
	#w = open(out, "w")
	words = Counter()
	globalC = Counter()
	prob = dict()

	flag = 0
	for line in reversed(open(file).readlines()):
		v = line.split("\t")
		if len(v) >= 2:
			if v[1] == toLookFor:
				flag = 1
			elif flag == 1:
				words[v[0]] += 1
				flag = 0


	for line in open(file).readlines():
		vl = line.split("\t")
		if len(vl) >= 2:
			globalC[vl[0]] += 1



	for item in words.keys():
		prob[item] = words[item]/float(globalC[item]) * 100

	sorted_x = sorted(prob.items(), key=operator.itemgetter(1))
	for item in sorted_x:
		print str(item) + " " + str(words[item[0]]) + " on " + str(globalC[item[0]])
		

concepts = ["B-actor.name","B-actor.nationality","B-actor.type","B-award.category","B-award.ceremony","B-character.name","B-country.name","B-director.name","B-director.nationality","B-movie.description","B-movie.genre","B-movie.gross_revenue","B-movie.language","B-movie.location","B-movie.name",
"B-movie.release_date","B-movie.release_region","B-movie.star_rating","B-movie.subject","B-person.name","B-person.nationality","B-producer.name","B-rating.name"]

for item in concepts:
	print "\n\n Concept: " + str(item)
	findInsights("NLSPARQL.test.data", "oo.txt", str(item)+"\n")
