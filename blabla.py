import sys
import chain

db_file = sys.argv[1]
num_of_words = int(sys.argv[2])

babble = Babbler(db_file)
word = babble.cur.execute('SELECT left_word, SUM(occurences) as occs FROM rels GROUP BY left_word ORDER BY occs DESC; ').fetchone()[0]
print(babble.babble(word, num_of_words, True))