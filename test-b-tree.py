# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:22:28 2020

@author: Hassan Zekkouri
"""
from Btree import *

t = BTree(3)


"""
t.insert(10)
t.insert(20)
t.insert(30)
t.insert(40)
t.insert(50)
t.insert(60)
t.insert(70)
t.insert(80)
t.insert(90)
"""

t.insert(10); 
t.insert(20); 
t.insert(5); 
t.insert(6); 
t.insert(12); 
t.insert(30); 
t.insert(7); 
t.insert(17); 
  

t.traverse()

print()
n = 2
if t.search(n): print(n,"Is in.")
else: print(n,"Is not in.")