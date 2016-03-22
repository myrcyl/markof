import sys
import sqlite3
import random

class Babbler:

	def __init__(self, db_file):
		self.conn = sqlite3.connect(db_file)
		self.cur = self.conn.cursor()

	def get_next_word(self, first_word):
		first_word = first_word.replace('\'', '\'\'')
		self.cur.execute('SELECT right_word, chance FROM rels WHERE left_word = \'%s\' ORDER BY chance DESC;' % (first_word))
		rows = self.cur.fetchall()
		rand_num = random.random()
		sum_of_chances = 0
		for row in rows:
			sum_of_chances = sum_of_chances + float(row[1])
			if rand_num <= sum_of_chances:
				word = row[0]
				return str(word)
		return None

	def babble(self, word, num_of_words, finish_at_period):
		result = word + ' '

		while word != None:
			word = self.get_next_word(word)
			result = result + word + ' '
			num_of_words = num_of_words - 1
			if (not finish_at_period or word[-1] == ".") and num_of_words <= 0:
				break
		return result

db_file = sys.argv[1]
num_of_words = int(sys.argv[2])

babble = Babbler(db_file)
word = babble.cur.execute('SELECT left_word, SUM(occurences) as occs FROM rels GROUP BY left_word ORDER BY occs DESC; ').fetchone()[0]
print(babble.babble(word, num_of_words, True))