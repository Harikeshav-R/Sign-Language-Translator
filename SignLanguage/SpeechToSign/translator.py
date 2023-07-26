import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tree import ParentedTree


class ISLConverter:
    def __init__(self):
        self.parser = nltk.parse.corenlp.CoreNLPParser(url='http://localhost:9000')
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words("english"))

    def find_leaf_position(self, parsed_tree: ParentedTree, subtree: ParentedTree) -> tuple:
        """
        Find the leaf position of the given subtree in the parse tree.

        Args:
            parsed_tree (ParentedTree): The parsed tree of the sentence.
            subtree (ParentedTree): The subtree whose position needs to be found.

        Returns:
            tuple: The leaf position of the subtree in the parse tree, or None if not found.
        """
        leaves = parsed_tree.leaves()
        try:
            subtree_index = leaves.index(subtree.leaves()[0])
            return parsed_tree.leaf_treeposition(subtree_index)[:-1]
        except ValueError:
            return None