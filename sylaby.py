vowels = "aeiouy"
letters = "aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż"

def syllabise(word):

	sylaby = []
	sylaba = ''

	i = 0
	for l in word:
		if l in letters:
			sylaba = sylaba + l
		if l in vowels and i + 2 != len(word) and (i + 1 != len(word) and word[i + 1] not in vowels) or i + 1 == len(word):
			sylaby.append(sylaba)
			sylaba = ''
		i = i + 1

	return sylaby