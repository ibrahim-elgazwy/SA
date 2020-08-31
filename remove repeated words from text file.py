# -*- coding: utf-8 -*-

lst = []        #this list store unique words
lst2 = []       #this list store all words
with open ("neg_words_all.txt") as f:
    for line in f:
        for word in line.split():
            lst2.append(word)
            for x in lst2:
                if x not in lst:
                    lst.append(x)
                    lst2.remove(x)

for w in lst:
    print (w.decode('utf-8'))
