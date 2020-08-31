# -*- coding: utf-8 -*-
'''Code to perform basic stemming of Arabic tweets
Input file <name>.txt; output <name>_normalised.txt'''
#################

import csv,re,sys
import string
import collections
import itertools
from regex import *
from tashaphyne import *

############

def getWordLists():
    
    '''Loads emoticons and words with assigned sentiments from file. Returns tuple of lists of words.'''
    stem=''
    stopWords=[line[0].decode('utf-8') for line in csv.reader(open(stem+'stop_words.txt','r'),delimiter='\t')]
    negationWords=[line[0].decode('utf-8') for line in csv.reader(open(stem+'negation_words.txt','r'),delimiter='\t')]
    exemptWords=[line[0].decode('utf-8') for line in csv.reader(open(stem+'exempt_words.txt','r'),delimiter='\t')]
    posEmojis=[line[0].decode('utf-8') for line in csv.reader(open(stem+'pos_emojis.txt','r'),delimiter='\t')]
    negEmojis=[line[0].decode('utf-8') for line in csv.reader(open(stem+'neg_emojis.txt','r'),delimiter='\t')]
    return stopWords,negationWords,exemptWords,posEmojis,negEmojis

############

def main():

    v=False
# Flag to print steps verbosely

    vv=False
# Flag to print out completed tweet

    try:
        inFileHandle=open(sys.argv[1],'r')
        outFile=csv.writer(open(sys.argv[1].partition('.')[0]+'_norm_Extr.txt','w'),delimiter='\t')

    except:
        print 'NEED FILE AS FIRST ARG'
        sys.exit(1)
        
    lines=[l.split('\t') for l in inFileHandle.readlines()]
    tweets=[l[0].decode('utf-8') for l in lines]
    stopWords,negationWords,exemptWords,posEmojis,negEmojis=getWordLists()
    emojis=posEmojis+negEmojis
    escapedEmojis=[e.replace('(','\(').replace(')','\)').replace('.','\.').replace('|','\|') for e in emojis]
    exemptCount=0
    links=collections.defaultdict(int)
    ats=collections.defaultdict(int)
    for tt,tweet in enumerate(tweets):
        if (tt+1)%20000==0:print tt+1,'PROCESSED....'
        tokens=re.sub(r'\r|\n','',tweet,re.U).split(r' ')
        if v:print '++++++++\nINPUT:\n',tweet,'\n',tokens,'\n++++++++'
        outTweet=[]
        
######################
        
        for w,word in enumerate(tokens):
            isAt=re.match(atRe,word,re.U)
            isHash=re.match(hashRe,word,re.U)
            isHttp=re.match(httpRe,word,re.U)
            isNeg=(word in negationWords)
            isStop=(word in stopWords)
            isExempt=(word in exemptWords)
            isEmoji=any([re.match(e,word,re.U) for e in escapedEmojis])

            if (isStop or isNeg or isExempt or isEmoji or isHttp or isHash):
                exemptCount+=1
##                if isEmoji:
##                    outTweet.append(word)
##                elif isNeg:
##                    outTweet.append(word)
            else:
                if not (isHttp or isAt or isEmoji):
        # Don't clean URLs or @-mentions
############
## Normalising
                    word=re.sub(puncRe,'',word)
                    word=re.sub(underscoreRe,' ',word)
                    word=strip_tatweel(word)
                    word=normalize_spellerrors(word)
                    

# Remove punctuation and line endings...
# ...but only if not emoji, otherwise keep
# it unchanged to be counted later

                    word=re.sub(harakatRe,u'',word,flags=re.U)
                    word=re.sub(u'آ',u'ا',word)
                    word=re.sub(alifRe,u'ا',word)   
                    word=re.sub(alifMaksourRe,u'ي',word)
                    word=re.sub(wawRe,u'و',word)
                    word=re.sub(hahRe,u'ة',word)
                    #word=re.sub(hahaRe,u'ههه',word)

############
## Stemming
                    word=re.sub(alRe,'',word)
                    word=re.sub(tuhaRe,u'ة',word)
                    word=re.sub(haRe,u'',word)
                    word=re.sub(verbSuffixesRe,'',word)
                    word=''.join(ch for ch, _ in itertools.groupby(word))
                    outTweet.append(unicode(word))
                    
                elif isHttp:
                    word=re.sub(httpCleanRe,'',word)
                    links[word]+=1
                elif isAt:
                    print '\t@-mention NOT CLEANING'
                    ats[word]+=1
                    
        # Count mentions and links

        for o in outTweet:
            if v:print o,
            if v:print ''
            if v:print '====================='
        outList=[o.encode('utf-8') for o in outTweet]+lines[tt][1:]
        outFile.writerow(outList)
        
    linkFile=csv.writer(open('links.csv','w'),delimiter='\t')
    for k,v in links.items():linkFile.writerow([v,k.encode('utf-8')])
if __name__=="__main__":
  main()
