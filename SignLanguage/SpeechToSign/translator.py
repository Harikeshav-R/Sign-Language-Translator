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

    def remove_unwanted_words(self, parsed_tree: ParentedTree) -> ParentedTree:
        """
        Remove unwanted parts of speech from the parse tree for Indian Sign Language (ISL) conversion.

        Args:
            parsed_tree (ParentedTree): The parsed tree of the sentence.

        Returns:
            ParentedTree: The parse tree with unwanted parts of speech removed.
        """
        unwanted_parts_of_speech = ["TO", "POS", "MD", "FW", "CC", "DT", "JJR", "JJS", "NNS", "NNPS", "RP", "SYM", "UH",
                                    "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "PDT", "PRP$", "PRP"]
        subtrees_to_remove = [subtree for subtree in
                              parsed_tree.subtrees(lambda t: t.label() in unwanted_parts_of_speech)]

        # Remove collected subtrees
        for subtree in subtrees_to_remove:
            if subtree in parsed_tree:
                parsed_tree.remove(subtree)

        return parsed_tree

    def convert_to_isl(self, input_string: str) -> str:
        """
        Convert an input English sentence to Indian Sign Language (ISL) sentence.

        Args:
            input_string (str): The input English sentence.

        Returns:
            str: The converted ISL sentence.
        """
        # Parse the English text
        english_tree = [tree for tree in self.parser.parse(input_string.split())]
        parse_tree = english_tree[0]
        parent_tree = ParentedTree.convert(parse_tree)

        # Reorder for ISL grammar needs
        reordered_tree = self.reorder_for_isl(parent_tree)

        # Remove unwanted words (parts of speech)
        cleaned_tree = self.remove_unwanted_words(reordered_tree)

        # Extract the lemmatized words
        parsed_sent = cleaned_tree.leaves()
        lemmatized_words = [self.stemmer.stem(w) for w in parsed_sent]

        # Remove stopwords
        isl_sentence = [w for w in lemmatized_words if w.lower() not in self.stop_words]

        # Identify and place the question word at the end of the sentence
        question_word = None
        for word in isl_sentence:
            if word in ["what", "when", "where", "why", "who", "how"]:
                question_word = word
                isl_sentence.remove(word)
                break

        if question_word:
            isl_sentence.append(question_word)

        return " ".join(isl_sentence)
