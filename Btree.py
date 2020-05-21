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
        # Print the subtree rooted with the last child
        if self.leaf == False:
            self.child[self.nk].traverse()     ########################
            
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
            if self.child[i].nk == 2*self.l-1:
                # Split
                self.splitChild(i, self.child[i])
                # 1. The mid key goes up
                # 2. Decide which half to have the new key
                if self.keys[i] < key: i+=1 # go right
            self.child[i].insertNonFull(key)
            
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
        print("[debug] finding a child")
        # Index of the leftmost key
        i = self.nk-1
        while i >= 0 and self.keys[i] > key:
            i -= 1
        # return child index
        return i+1
        
            
        
    def splitChild(self, i, y):
        print("[debug] spliting a child")
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
        
    #_____________________ Deletion part _________________________
    
    def findKey(self, key):
        """
        A function that returns the index of the first key that is greater 
        or equal to k
        """
        idx = 0
        while idx < self.nk and self.keys[idx] < key: idx += 1
        return idx
            
    
    def remove(self, key):
        """
        A wrapper function to remove the key k in subtree rooted with 
        this node. 
        """
        idx = self.findKey(key)
        
        # If the key is in the current node
        if idx < self.nk and self.keys[idx] == key:
            if self.leaf: 
                self.removeFromLeaf(idx)
            else:
                self.removeFromNonLeaf(idx)
        else:
            # If the current node is leaf, then the key
            # is not present in tree
            if self.leaf:
                print("[Exception] the key {} is not present in the tree.".format(key))
                return
            
            # The key to be removed is present in the sub-tree rooted with this node 
            # The flag indicates whether the key is present in the sub-tree rooted 
            # with the last child of this node
            flag = (idx == self.nk)
            
            # If the child where the key is supposed to exist has less that (l) keys, 
            # we fill that child 
            if self.child[idx].nk < self.l: self.fill(idx)
            
            # If the last child has been merged, it must have merged with the previous 
            # child and so we recurse on the (idx-1)th child. Else, we recurse on the 
            # (idx)th child which now has atleast (l=L) keys 
            if flag and idx > self.nk: 
                self.child[idx-1].remove(key)
            else: self.child[idx].remove(key)
        
                
                
    
    def removeFromLeaf(self, idx):
        """
        A function to remove the key present in idx-th position in 
        this node which is a leaf (the sweetest cake!)
        """
        # Crush the keys[idx] by moving all keys after
        # it one place backward
        for i in range(idx+1, self.nk): self.keys[i-1] = self.keys[i]
        # Reduce the number of keys
        self.nk -= 1

    def removeFromNonLeaf(self, idx):
        """
        A function to remove the key present in idx-th position in 
        this node which is a non-leaf node 
        """
        k = self.keys[idx]
        
        # If the child that precedes k (child[idx]) has atleast (l) keys, 
        # find the predecessor 'pred' of k in the subtree rooted at 
        # child[idx]. Replace k by pred. Recursively delete pred in child[idx]
        if self.child[idx].nk >= self.l:
            pred = self.getPred(idx)
            self.keys[idx] = pred
            self.child[idx].remove(pred)
        
            # If the child[idx] has less that t keys, examine child[idx+1]. 
            # If child[idx+1] has atleast (l) keys, find the successor 'succ' of k in 
            # the subtree rooted at child[idx+1] 
            # Replace k by succ 
            # Recursively delete succ inchildC[idx+1]
        elif self.child[idx+1].nk >= self.l:
            succ = self.getSucc(idx)
            self.keys[idx] = succ
            self.child[idx+1] .remove(succ)
            
            # If both child[idx] and child[idx+1] has less that t keys,
            # merge k and all of child[idx+1]into child[idx]
            # Now child[idx] contains 2l-1 keys
            # Free child[idx+1] and recursively delete k from child[idx] 
        else:
            self.merge(idx)
            self.child[idx].remove(k)
        
    
    def getPred(self, idx):
        """
        A function to get the predecessor of the key- where the key 
        is present in the idx-th position in the node 
        """
        pass
    
    def getSucc(self, idx):
        """
         A function to get the successor of the key- where the key 
         is present in the idx-th position in the node
        """
        pass
    
    def fill(self, idx):
        """
        A function to fill up the child node present in the idx-th 
        position in the C[] array if that child has less than t-1 keys  
        """
        pass
    
    def borrowFromPrev(self, idx):
        """
        A function to borrow a key from the C[idx-1]-th node and place 
        it in C[idx]th node 
        """
        pass
    
    def borrowFromNext(self, idx):
        """
        A function to borrow a key from the C[idx+1]-th node and place it 
        in C[idx]th node 
        """
        pass
    
    def merge(self, idx):
        """
        A function to merge idx-th child of the node with (idx+1)th child of 
        the node 
        """
        pass
    
    
    
    
    
    
    

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
            print("[debug] inserting first key...")
            # Create the root
            self.root = Node(self.l, True)
            self.root.keys[0] = key
            self.root.nk = 1
        else:
            # If root is full,then the tree grows in height
            # means, we split
            if self.root.nk == 2*self.l-1:
                print("[debug] splitting...")
                # Create a new root
                nr = Node(self.l, False)
                
                # Add old root as its child
                nr.child[0] = self.root
                
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
                print("[debug] insertNonFull...")
                self.root.insertNonFull(key)
                
    def remove(self, key):
        """ 
        This function removes key from the B tree
        """
        # Check if tree is empty
        if self.root == None:
            print("[Exception] The tree is empty.")
            return
        # Start from root
        self.root.remove(key)
        
        # If the root has 0 keys now (means key was in root by itself)
        # make its 1st child as the new root if it exists, otherwise
        # set root as None (tree becomes empty)
        if self.root.nk == 0:
            tmp = self.root
            if self.root.leaf:
                self.root = None
            else:
                self.root = self.root.child[0]
            # free
            del tmp
        
        
            
                
                
    
            
        
    
    
    