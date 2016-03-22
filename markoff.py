import sys
import sqlite3
import math
import sylaby

db_file = sys.argv[2]
in_file = sys.argv[1]

conn = sqlite3.connect(db_file)
cur = conn.cursor()

in_file = sys.argv[1]
text = open(in_file).read().replace('\'', '\'\'')
words = text.split()

num_of_words = len(words)
percent = 0
percent_step = math.floor(float(num_of_words) / 100.0)
step_counter = 0

cur.execute('CREATE TABLE IF NOT EXISTS rels ("left_word" TEXT NOT NULL, "right_word" TEXT NOT NULL, "chance" REAL NOT NULL DEFAULT (0), "occurences" INTEGER NOT NULL DEFAULT (0), PRIMARY KEY("left_word", "right_word"))')

pairs = []

for i in range(0, num_of_words - 1):
	left_word = words[i].strip()
	right_word = words[i + 1].strip()
	pairs.append((left_word, right_word))

cur.executemany('INSERT INTO rels (left_word, right_word, occurences) SELECT ?, ?, 0 WHERE NOT EXISTS (SELECT 1 FROM rels WHERE left_word = ? AND right_word = ?);', [(x[0], x[1], x[0], x[1]) for x in pairs])
cur.executemany('UPDATE rels SET occurences = occurences + 1 WHERE left_word = ? AND right_word = ?;', pairs)

cur.execute('UPDATE rels SET chance = occurences * 1.0 / (SELECT SUM(r2.occurences) FROM rels r2 WHERE r2.left_word = rels.left_word);')
conn.commit()