import sys
import Queue
import subprocess
from subprocess import Popen

# Directories
Data = "data/"
Scrap = "scrap/"
# Filenames
Trainingset = "NLSPARQL.train.data"
Testset = "NLSPARQL.test.data"

def replaceLabelsIn(items, orig, gen, placeholder, concept):
	items = items.split(',')
	# Length of the sequence of words whose concepts are to be replaced
	seq_len = len(items) - 1
	# This will hold the other items - initialized as empty
	w = list()
	for i in range(0, seq_len):
		w.append('')
	# List of indexes of words whose concepts are to be replaced
	indexes = list()
	# Queues that keep track of words and concepts in sentences
	sentence = Queue.Queue()
	tags = Queue.Queue()
	# Index of the current word in the sentence that will be parsed
	index = -1
	# Open files
	g = open(gen, "w")
	with open(orig, "r") as f:
		for line in f:
			words = line.split('\t')
			# If we're not in an empty line - parse sentence
			if len(words) > 1:
				index += 1
				current = words[0]
				tag = words[1]
				# Remove new lines from tags
				tag = tag[0 : len(tag)-1]
				sentence.put(current)
				tags.put(tag)
				# This cycle updates the sequence of words that we're considering while we're scanning the sentence
				if tag.find('B-' + concept) < 0:
					for i in range(0, seq_len):
						if i == (seq_len - 1):
							# Save word in sequence only if it is a valid word - tagged as 'O'
							if tag == 'O':
								w[i] = current
							else:
								w[i] = ''
						else:
							w[i] = w[i+1]
				# If we've met the concept, we check if the previous words are the sequence we expect them to be
				else:
					replace_words = True
					for j in range(0, len(w)):
						# If one of the previous words doesn't match the sequence, we don't replace the tags
						if items[j] != w[j]:
							replace_words = False
							break
					# If we have to replace words' tags, we save the indexes of these words
					if replace_words == True:
						for j in range(1, len(w) + 1):
							indexes.append(index - j)
			# Empty line - end of sentence, time to replace tags if the conditions are met
			else:
				for j in range(0, index + 1):
					curr_w = sentence.get()
					curr_t = tags.get()
					# If we're not at a word of whom we want to replace the tag, we simply write that word and its tag
					if j not in indexes:
						g.write('%s\t%s\n' % (curr_w, curr_t))
					# Otherwise we replace the tag
					elif replace_words == True:
						g.write('%s\t%s\n' % (curr_w, placeholder))
				# Write empty line for end of sentence
				g.write('\n')
				# Reset variables
				index = -1
				indexes[:] = []
	g.close()

def generateCopy(orig, copy):
	g = open(copy, "w")
	with open(orig, "r") as f:
		for line in f:
			words = line.split('\t')
			if len(words) > 1:
				g.write('%s\t%s' % (words[0], words[1]))
			else:
				g.write('\n')
	g.close()

## MAIN ##

original_trainset = Data + Trainingset
original_testset = Data + Testset
temp_trainset = Scrap + 'temp_train.data'
temp_testset = Scrap + 'temp_test.data'
generated_trainset = Scrap + Trainingset
generated_testset = Scrap + Testset

generateCopy(original_trainset, temp_trainset)

user_input = sys.argv[1].split('-')

placeholder = 0

# Generate a dictionary of placeholders for each concept
placeholders = dict()
for elements in user_input:
	elements = elements.split(',')
	key = elements[len(elements)-1]
	if key not in placeholders.keys():
		placeholders[key] = '$%d' % placeholder
		placeholder += 1

for items in user_input:
	current_concept = items.split(',')
	current_concept = current_concept[len(current_concept)-1]
	replaceLabelsIn(items, temp_trainset, generated_trainset, placeholders[current_concept], current_concept)
	generateCopy(generated_trainset, temp_trainset)
