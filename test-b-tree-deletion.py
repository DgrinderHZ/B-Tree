# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:44:07 2020

@author: Hassan Zekkouri
"""

import Btree 

t = Btree.BTree(3)

toInsert = [1,3,7,10,11,13,14,15,18,16,19,24,25,26,21,4,5,20,22,2,17,12,6]
for n in toInsert: t.insert(n)

print("================== Traversal of tree constructed is\n")
t.traverse()

toRemove =[6, 14, 7, 4, 2, 16]
for n in toRemove:
    t.remove(n)
    print("\n================== Traversal of tree after {} being removed\n".format(n))
    t.traverse()