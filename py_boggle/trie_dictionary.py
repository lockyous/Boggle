import typing
from typing import Optional, Dict
from collections.abc import Iterator

from py_boggle.boggle_dictionary import BoggleDictionary


class TrieNode:
    """
    Our TrieNode class. Feel free to add new properties/functions, but 
    DO NOT edit the names of the given properties (children and is_word).
    """
    def __init__(self):
        self.children : Dict[str, TrieNode] = {} # maps a child letter to its TrieNode class
        self.is_word = False # whether or not this Node is a valid word ending


class TrieDictionary(BoggleDictionary):
    """
    Your implementation of BoggleDictionary.
    Several functions have been filled in for you from our solution, but you are free to change their implementations.
    Do NOT change the name of self.root, as our autograder will manually traverse using self.root
    """

    def __init__(self):
        self.root : TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        # Remember to add every word to the trie, not just the words over some length.
        with open(filename) as wordsfile:
            for line in wordsfile:
                word = line.strip().lower()

                # create nodes for each letter and mark node as the end of each word
                cur_trie_node = self.root
                for char in word:
                    if char not in cur_trie_node.children:
                        cur_trie_node.children[char] = TrieNode()

                    cur_trie_node = cur_trie_node.children[char]

                cur_trie_node.is_word = True


    def traverse(self, prefix: str) -> Optional[TrieNode]:
        """
        Traverse will traverse the Trie down a given path of letters `prefix`.
        If there is ever a missing child node, then returns None.
        Otherwise, returns the TrieNode referenced by `prefix`.
        """
        cur_trie_node = self.root

        for char in prefix.lower():
            if char not in cur_trie_node.children:
                return None

            cur_trie_node = cur_trie_node.children[char]
        return cur_trie_node

    def is_prefix(self, prefix: str) -> bool:
        cur_trie_node = self.traverse(prefix)
        return cur_trie_node is not None


    def contains(self, word: str) -> bool:
        cur_trie_node = self.traverse(word)
        if cur_trie_node is None:
            return False
        return cur_trie_node.is_word

    def __iter__(self) -> typing.Iterator[str]:

        #Traverse Tire recursively in alphabetical order and yield complete words
        def trav_words(cur_trie_node, word):
            if cur_trie_node.is_word:
                yield word

            for char in sorted(cur_trie_node.children.keys()):
                yield from trav_words(cur_trie_node.children[char], word + char)

        return trav_words(self.root, "")
