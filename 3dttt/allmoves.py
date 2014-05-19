#!/usr/bin/env python3

# Dump all possible moves on the 3d board
# mal <mal@sec.gd>

for a in range(0,3):
    for b in range(0,3):
       for c in range(0,3):
           print(a,b,c,sep=',')

