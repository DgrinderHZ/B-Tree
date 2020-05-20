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
    
    def makePlace(self, key):
        """
        This function does two things 
            a) Finds the location of new key to be inserted 
            b) Moves all greater keys to one place ahead
        """
        # Index of the leftmost key
        i = self.nk-1
        # Move keys forward one position each
        while i >= 0 and self.keys[i] > key:
            self.keys[i+1] = self.keys[i]
            i -= 1
        # return key position
        return i+1
        
    def findChild(self, key):
        """
        Find the child which is going to have the new key
        """
        # Index of the leftmost key
        i = self.nk-1
        while i >= 0 and self.keys[i] > key:
            i -= 1
        # return child index
        return i+1
        
    
    def insertNonFull(self, key):
        """
         A utility function to insert a new key in the subtree rooted with 
         this node. The assumption is, the node must be non-full when this 
         function is called
         ______________________________
         
         key: The key to be inserted
        """
        # If its a leaf node
        if self.leaf:
            i = self.makePlace(key)
            # Insert
            self.keys[i] = key
            self.nk += 1
        else: # Internal node
            i = self.findChild(key)
            # If child[i] is full
            if self.child[i].nk == 2*self.nk-1:
                # Split
                self.splitChild(i, self.child[i])
                # 1. The mid key goes up
                # 2. Decide which half to have the new key
                if self.keys[i] < key: i+=1 # go right
            self.child[i].insertNonFull(key)

                    
                    
            
            
            
        
    def splitChild(self, i, y):
        """
        A utility function to split the child y of this node. i is index of y in 
        child array C[].  The Child y must be full when this function is called 
        __________________________
        i :
        y :
            
        """
        # Create right node
        right = Node(y.l, y.leaf)
        right.nk = self.l-1
        
        # Copy the last (l-1) keys of y to right node
        for j in range(self.l-1):
            right.keys[j] = y.keys[j + self.l]
        
        # Copy the last (l) children of y to right node
        if y.leaf == False:
            for j in range(self.l):
                right.child[j] = y.child[j + self.l]
        
        # Reduce the nbr of keys in y (left node)
        y.nk = self.l - 1
        
        # Since the current node is having a new child,
        # make space for it (shift)
        for j in range(self.nk, i, -1): self.child[j+1] = self.child[j]
        
        # Add the new child to the current node
        self.child[i+1] = right
        
        # A key will move up from y to this node. Find it a location
        # to be inserted in and shift all greater keys forward one space ahead
        for j in range(self.nk-1, i-1, -1): self.keys[j+1] = self.keys[j]
        # Insert the mid key (move it up)
        self.keys[i] = y.keys[self.l-1]
        # Update nk
        self.nk += 1
        
            
    
    

class BTree():
    def __init__(self, l):
        self.root = None # a Node
        self.l = l
    
    def traverse(self):
        if self.root != None:
            self.root.traverse()
    
    def search(self, key):
        return (None if self.root == None else self.root.search(key))
    
    def insert(self, key):
        # If the tree is empty
        if self.root == None:
            # Create the root
            self.root = Node(self.l, True)
            self.root.keys[0] = key
            self.root.nk = 1
        else:
            # If root is full,then the tree grows in height
            # means, we split
            if self.root.nk == 2*self.l-1:
                # Create a new root
                nr = Node(self.l, False)
                
                # Add old root as its child
                nr.child[0] = nr
                
                # Split the old root then move one key up
                nr.splitChild(0, self.root)
                
                # Decide which of the 2 children is going
                # to have a new key
                i = 0
                if nr.keys[0] < key: i += 1
                nr.child[i].insertNonFull(key)
                
                # Update root
                self.root = nr
            else:
                self.root.insertNonFull(key)
                
                
    
            
        
    
    
    