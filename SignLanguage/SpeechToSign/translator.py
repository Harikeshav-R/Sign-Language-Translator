import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tree import ParentedTree


class ISLConverter:
    def __init__(self):
        self.parser = nltk.parse.corenlp.CoreNLPParser(url='http://localhost:9000')
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words("english"))

    def find_leaf_position(self, parsed_tree: ParentedTree, subtree: ParentedTree) -> tuple | None:
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

    def reorder_for_isl(self, parsed_tree: ParentedTree) -> ParentedTree:
        """
        Reorder the parse tree for Indian Sign Language (ISL) grammar needs.

        Args:
            parsed_tree (ParentedTree): The parsed tree of the sentence.

        Returns:
            ParentedTree: The reordered parse tree.
        """
        # Find NP and VP subtrees in the parse tree
        noun_phrases = [subtree for subtree in parsed_tree.subtrees(lambda t: t.label() == "NP")]
        verb_phrases = [subtree for subtree in parsed_tree.subtrees(lambda t: t.label() == "VP")]

        # Rearrange VP subtrees to the right of the corresponding NP subtrees
        for np_subtree, vp_subtree in zip(noun_phrases, verb_phrases):
            # Get the positions of NP and VP subtrees
            np_position = self.find_leaf_position(parsed_tree, np_subtree)
            vp_position = self.find_leaf_position(parsed_tree, vp_subtree)

            # Rearrange VP subtree to the right of the NP subtree
            if np_position and vp_position and vp_position[-1] < np_position[-1]:
                del parsed_tree[vp_position]
                parsed_tree[np_position[-1] + 1:np_position[-1] + 1] = [vp_subtree]

        return parsed_tree