#!/usr/bin/env python3
tab = []
info = 1
for i in range(1, 1001):
    tab.append(i)
    pass
while len(tab) > 1:
    for i in range(1, int(len(tab)/2)+1):
        print(tab[i])
        print(i)
        tab.pop(i)
        pass
    print(tab)
    pass
