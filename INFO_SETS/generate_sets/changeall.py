
def changeInsights(file, out):
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

changeInsights("NLSPARQL.train.data", "oo.txt")
'''
r = open ("yes.txt","w")
for line in reversed(open("oo.txt").readlines()):
	r.write(line)
r.close()
'''