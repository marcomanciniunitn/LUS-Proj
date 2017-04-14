
def changeInsights(file, out):
	w = open(out, "w")

	flag=0
	for line in reversed(open(file).readlines()):
		v = line.split("\t")
		if(len(v)>1):
			if v[1][0:1] == "B":
				w.write(line)
				flag = 1
			elif v[1][0:1] == 'O' and flag == 1:
				w.write(v[0] + "\t" + "$-"+str(v[0])+"\n")
				flag = 2
			elif v[1][0:1] == 'O' and flag == 2:
				w.write(v[0] + "\t" + "$-"+str(v[0])+"\n")
				flag = 0
			else:
				w.write(line)
				flag=0
		else:
			w.write("\n")
			flag = 0

	w.close()

changeInsights("NLSPARQL.train.data", "oo.txt")
r = open ("yes.txt","w")
for line in reversed(open("oo.txt").readlines()):
	r.write(line)
r.close()