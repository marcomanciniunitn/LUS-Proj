import sys
from collections import Counter	
import operator

def change(file, out):
	f = open(file, "r")
	wr = open(out, "w")
	flag = 0

	for line in f:
		
		if line == "prod\n":
			wr.write(line)
			flag=1
		elif line == "dir\n":
			wr.write(line)
			flag = 2
		elif line == "by\n" and flag == 1:
			wr.write("by.prod\n")
			flag = 0
		elif line == "by\n" and flag == 2:
			wr.write("by.dir\n")
			flag=0
		else:
			wr.write(line)

	f.close()
	wr.close()


def change2(file,out):
	arr = list()
	w = open(out, "w")

	flag = 0

	for line in reversed(open(file).readlines()):
		if line == "B-producer.name\n":
			w.write(line)
			flag = 1
		elif line == "B-director.name\n":
			w.write(line)
			flag = 2
		elif line == "by\n" and flag == 1:
			w.write("by.prod\n")
			flag = 0
		elif line == "by\n" and flag == 2:
			w.write("by.dir\n")
			flag=0
		else:
			w.write(line)

	w.close()

#REMEMBER  \n
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
		

def changeInsights(file, out, item):
	w = open(out, "w")

	flag = 0
	for line in reversed(open(file).readlines()):
		v = line.split("\t")
		if(len(v)>1):
			if v[1] == item[0]:
				w.write(line)
				flag = 1
			elif v[1] == item[1]:
				w.write(line)
				flag = 2
			elif v[1] == item[2]:
				w.write(line)
				flag = 3
			elif v[1] == item[3]:
				w.write(line)
				flag = 4
			elif v[0] == 'starring' and flag == 1:
				w.write(v[0] + "\t" + "act\n")
				flag = 0
			elif v[0] == 'rated' and flag == 2:
				w.write(v[0] + "\t" + "rate\n")
				flag = 0
			elif v[0] == 'played' or v[0] == 'plays' and flag == 3:
				w.write(v[0] + "\t" + "gioc\n")
				flag = 0
			elif v[0] == 'movie'and flag == 4:
				w.write(v[0] + "\t" + "movie\n")
				flag = 0
			else:
				w.write(line)
		else:
			w.write("\n")

	w.close()

aaa = ["B-actor.name","B-actor.nationality","B-actor.type","B-award.category","B-award.ceremony","B-character.name","B-country.name","B-director.name","B-director.nationality","B-movie.description","B-movie.genre","B-movie.gross_revenue","B-movie.language","B-movie.location","B-movie.name",
"B-movie.release_date","B-movie.release_region","B-movie.star_rating","B-movie.subject","B-person.name","B-person.nationality","B-producer.name","B-rating.name"]

aa = ["B-country.name", "B-movie.location", "B-movie.release_region", "B-director.nationality","B-movie.language"]

#change2("train_tmp.txt", "train2_tmp.txt")

#r = open ("yes.txt","w")
#for line in reversed(open("train2_tmp.txt").readlines()):
	#r.write(line)
#r.close()

#change3("NLSPARQL.train.data", "aa")
for item in aaa:
	print "\n\n Concept: " + str(item)
	findInsights("NLSPARQL.test.data", "oo.txt", str(item)+"\n")

#aaa = ["B-rated.name\n","B-movie.name\n","B-character.name\n","B-actor.name\n"]
#findInsights("NLSPARQL.train.data", "oo.txt", aaa)
#r = open ("yes.txt","w")
#for line in reversed(open("oo.txt").readlines()):
#	r.write(line)
#r.close()