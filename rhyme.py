import sys
import sqlite3
import random
import sylaby

def get_next_word(first_word):
	first_word = first_word.replace('\'', '\'\'')
	cur.execute('SELECT right_word, chance FROM rels WHERE left_word = \'%s\' ORDER BY chance DESC;' % (first_word))
	rows = cur.fetchall()
	rand_num = random.random()
	sum_of_chances = 0
	for row in rows:
		sum_of_chances = sum_of_chances + float(row[1])
		if rand_num <= sum_of_chances:
			word = row[0]
			return str(word)
	return None

def get_next_line(last_word, num_of_syls, rhymes, depth):
	csyl = 0
	words = []
	if (rhymes):
		last_syl = sylaby.syllabise(last_word)[-1]
	next_word = last_word
	while csyl < num_of_syls:
		next_word = get_next_word(next_word)
		words.append(next_word)
		csyl = csyl + len(sylaby.syllabise(next_word))
	if csyl == num_of_syls:
		if not rhymes:
			return words
		else:
			next_last_syl = sylaby.syllabise(next_word)[-1]
			if next_last_syl == last_syl:
				return words
			else:
				if depth >= 25:
					#if len(next_last_syl) > 0 and len(last_syl) > 0 and next_last_syl[-1] == last_syl[-1]:
					#	return words
					last_syls = len(sylaby.syllabise(next_word))
					cur.execute("SELECT left_word FROM rels WHERE left_word LIKE '%" + last_syl + "' AND LOWER(left_word) <> LOWER('" + last_word + "')")
					result = cur.fetchone()
					if result != None:
						words = words[:-1] + [result[0]]
						return words
					else:
						return words
				else:
					return get_next_line(last_word, num_of_syls, rhymes, depth + 1)
	else:
		return get_next_line(last_word, num_of_syls, rhymes, depth + 1)

word = sys.argv[1]
db_file = sys.argv[2]
num_of_lines = int(sys.argv[3])
num_of_syls = int(sys.argv[4])
should_rhyme = True if int(sys.argv[5]) == 1 else False

conn = sqlite3.connect(db_file)
cur = conn.cursor()

rhymes = False

last_word = word
while num_of_lines > 0:
	line = get_next_line(last_word, num_of_syls, rhymes, 0)
	last_word = line[-1]
	num_of_lines = num_of_lines - 1
	rhymes = not rhymes if should_rhyme else rhymes
	print(' '.join(line))