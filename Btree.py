# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:11:40 2020

@author: Hassan Zekkouri
"""

class Node():
    def __init__(self, l, leaf):
        """
        Class: A B-Tree Node:
        keys: Array of keys
        l: Minimum degree L, Maximum degree is U=2*l-1
        child: Array of children
        nk: Number of keys, M=nk+1 the number of children
        """
        self.keys = [0 for _ in range(2*l-1)]
        self.l = l 
        self.child = [None for _ in range(2*l)]
        self.nk = 0
        self.leaf = leaf
    
    def traverse(self):
        """ Treverses all nodes in a subtree
        rooted with the current node.
        """
        for i in range(self.nk):
            # If the current node is not leaf,
            # traverse the subtree rooted with child[i]
            # then print keys[i]
            if self.leaf == False:
                self.child[i].traverse()
            print(self.keys[i], end=" ")
        # Print the subtree rooted with the lat child
        if self.leaf == False:
            self.child[-1].traverse()
            
    def search(self, key):
        """Searches key in a subtree rooted
        with the current node.
        """
        # Find the 1st key[i] ge to key
        i = 0
        while i < self.nk and key > self.keys[i]:
            i += 1
        # If Found
        if self.keys[i] == key: return self
        # If is leaf
        if self.leaf: return None
        
        # Otherwise Look elsewhere
        return self.child[i].search(key)

class BTree():
    def __init__(self, l):
        self.root = None # a Node
        self.l = l
    
    def traverse(self):
        if self.root != None:
            self.root.traverse()
    
    def search(self, key):
        return (None if self.root == None else self.root.search(key))
        
    
            
        
    
    
    