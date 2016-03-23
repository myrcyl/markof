import requests
from bs4 import BeautifulSoup
import sys
import markoff
import chain
import re

page = sys.argv[1]
db_file = sys.argv[2]
num_of_words = int(sys.argv[3])

r = requests.get(page)
soup = BeautifulSoup(r.text, 'html.parser')
ps = soup.find(class_='comments-stream').find_all('p')
joined = ''.join([x.text for x in ps])
joined = re.sub(r"([+|-]\d+)|0", "", joined)
joined = re.sub(r"@[a-zA-z0-9_-]+:", "", joined)
markoff.teach(db_file, joined.replace('\'', '\'\''))
babble = chain.Babbler(db_file)
word = babble.cur.execute('SELECT left_word, SUM(occurences) as occs FROM rels GROUP BY left_word ORDER BY occs DESC; ').fetchone()[0]
print(babble.babble(word, num_of_words, True))