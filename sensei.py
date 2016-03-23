import sys
import markoff

db_file = sys.argv[2]
in_file = sys.argv[1]

text = open(in_file).read().replace('\'', '\'\'')

teach(db_file, in_file)