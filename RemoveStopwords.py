from nltk.corpus import stopwords
from py2neo import Graph,authenticate
import re, string
import string

# default uri for local Neo4j instance
#authenticate("localhost:7474", "neo4j", "divyang001")
graphdb = Graph('http://neo4j:neo4j@localhost:7474/db/data',user='neo4j', password='divyang001')

# parameterized Cypher query for data insertion
# t is a query parameter. a list with two elements: [word1, word2]
INSERT_QUERY = '''
    FOREACH (t IN {wordPairs} |
        MERGE (w0:Word {word: t[0]})
        MERGE (w1:Word {word: t[1]})
        CREATE (w0)-[:NEXT_WORD]->(w1)
        )
'''
# arrifySentence("Hi there, Bob!) = [["hi", "there"], ["there", "bob"]]
def arrifySentence(sentence):
    sentence = sentence.lower()
    sentence = sentence.strip()
    exclude = set(string.punctuation)
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    sentence = regex.sub('', sentence)
    wordArray = sentence.split()
    filtered_words =[word for word in wordArray if (word not in stopwords.words('english') and len(word)>1)]
    finalset = set(filtered_words)
    filtered_words = list(finalset)
    tupleList = []
    for i, word in enumerate(filtered_words):
        if i+1 == len(filtered_words):
            break
        tupleList.append([word, filtered_words[i+1]])
    return tupleList

def main():
    tx = graphdb.begin()
    with open('try.txt') as f:
        count = 0
        for l in f:
            params = {'wordPairs': arrifySentence(l)}
            tx.append(INSERT_QUERY, params)
            tx.process()
            count += 1
            # process in batches of 100 insertion queries
            if count > 100:
                tx.commit()
                tx = graphdb.begin()
                count = 0
    f.close()
    tx.commit()









def main23():

	oldfile = "try.txt"
	newfile = "rem.txt"
	filtered_words = []
	with open(newfile, 'w') as outfile, open(oldfile, 'r') as infile:
		for line in infile:
			line=line.translate(None, string.punctuation)
			word_list = line.split()
			filtered_words =filtered_words+ [word for word in word_list if (word not in stopwords.words('english') and len(word)>1)]

	finalset = set(filtered_words)
	filtered_words = list(finalset)
	print filtered_words




if __name__ == '__main__':
		main()	


