import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tree import ParentedTree


class ISLConverter:
    def __init__(self):
        self.parser = nltk.parse.corenlp.CoreNLPParser(url='http://localhost:9000')
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words("english"))
