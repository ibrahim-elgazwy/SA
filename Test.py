# -*- coding: utf-8 -*-
'''Code to assign sentiment to Arabic tweets by counting terms
~22.5m to process 400k tweets on Macbook Pro'''
#################
import csv,re,sys
import numpy as np
#import matplotlib.pyplot as plt
import time,normalise_file
stem=''

###########
def getWordLists():
###########
    '''Reads terms to be tsted against text from files. Returns tuple of lists of words.'''
    posFile=csv.reader(open(stem+'pos_words.txt','r'),delimiter='\t')
    negFile=csv.reader(open(stem+'neg_words_all.txt','r'),delimiter='\t')
    intenSefier=csv.reader(open(stem+'intensfire.txt','r'),delimiter='\t')
    stopFile=csv.reader(open(stem+'stop_words.txt','r'),delimiter='\t')
    negationFile=csv.reader(open(stem+'negation_words.txt','r'),delimiter='\t')

    posEmojiFile=csv.reader(open(stem+'pos_emojis.txt','r'),delimiter='\t')
    negEmojiFile=csv.reader(open(stem+'neg_emojis.txt','r'),delimiter='\t')

    posWords=[line[0].encode('utf-8').decode('cp1256') for line in posFile if len(line)>0]
    negWords=[line[0].encode('utf-8').decode('cp1256') for line in negFile if len(line)>0]
    intensfierWords=[line[0].encode('utf-8').decode('cp1256') for line in intenSefier if len(line)>0]
    stopWords=[line[0].encode('utf-8').decode('cp1256') for line in stopFile if len(line)>0]
    negationWords=[line[0].encode('utf-8').decode('cp1256') for line in negationFile if len(line)>0]

    posEmojis=[line[0].encode('utf-8').decode('cp1256') for line in posEmojiFile if len(line)>0]
    negEmojis=[line[0].encode('utf-8').decode('cp1256') for line in negEmojiFile if len(line)>0]

    posEmojis=[re.escape(e) for e in posEmojis]
    negEmojis=[re.escape(e) for e in negEmojis]

    return posWords,negWords,intensfierWords,stopWords,negationWords,posEmojis,negEmojis

###########

def main():
    tn=0
    fp=0
    tp=0
    fn=0
    posCount=0
    negCount=0
    intensity=0
    stopCount=0
    negationCount=0
    y=0
    x=0
    negw =[]
    posw=[]

    try:
        inFileHandle=open('original_normalised.txt','r')
        tested_tweet=open('original.txt','r')
    except:
        print ('NEED FILE AS FIRST ARG')
        sys.exit(1)

    v=False
    # Flag to print verbosely

    if len(sys.argv)>2:
        v=True
        # Set verbose logging

    original_tweet=[s.encode('utf-8').decode('cp1256') for s in tested_tweet.readlines()]
    tweets=[t.encode('utf-8').decode('cp1256') for t in inFileHandle.readlines()]
    posWords,negWords,intensfierWords,stopWords,negationWords,posEmojis,negEmojis=getWordLists()


########################

    positives=np.zeros(shape=len(tweets))
    negatives=np.zeros(shape=len(tweets))
    c=0
    for t,tweet in enumerate(tweets):
        if (t+1)%100000==0:print (t+1,'PROCESSED....')

        posCount=negCount=stopCount=negationCount=0
        for w,word in enumerate(tweet.split('\t')):

            if v:print (word)
            
            if word in negationWords:
                negationCount+=1

            if word in posWords:
                posCount+=1
                posw.append(word)

            if word in negWords:
                negCount+=1
                negw.append(word)

            if word in intensfierWords:
                intensity+=1

            if word in stopWords:
                stopCount+=1
                
                if v:print (' => STOP')
                if v:print (' => NEGATION')

            if any([re.match(r'('+e+r')+',word,re.U) for e in posEmojis]):
                posCount+=1
                if v:print (' => POS EMOJI')
            if any([re.match(r'('+e+r')+',word,re.U) for e in negEmojis]):
                negCount+=1
                if v:print (' => NEG EMOJI')

##        if negationCount >0:
##            if (posCount - negCount) <0:
##                posCount*=20
##                negCount*=(-20)
##                x = ((posCount-negCount)+ 100)/2
##                y=max(x,10)
##            elif (posCount - negCount) >0:
##                posCount*=20
##                negCount*=(-20)
##                x = ((posCount-negCount)- 100)/2
##                y=min(x,10)
##            
##        print y
                
        if negationCount > 0:
            if negCount > posCount:
                
                if negCount >1:
                    negCount+=1.2
                posCount+=2
                
            if negCount < posCount:
                
                if posCount >1:
                    posCount+=1.2
                negCount+=2
                
        Sum = posCount 
        
        def result():
            s=""
            if  Sum > negCount:
                s="postive"
                
            elif Sum < negCount:
                s="negative"
                
            else:
                s="neutral"
                
            return s
            
                
            
        print ("===============================================================================")
        print ("                          Review n# " ,c, "                                    ")
        print ("===============================================================================" )   
        print(original_tweet[c])

        c=c+1
        print (c,':','(pos,neg,intens,stop,negation) = ',(posCount,negCount,intensity,stopCount,negationCount),'----  ''final_sentiment: ',result())
##        for w in posw:
##            print w
##        for w in negw:
##            print "negw",w 

##        if (result() == "negative"):
##            tn+=1
##        else:
##            fp+=1
        if (result() == "postive"):
            tp+=1
        else:
            fn+=1
            
        
        time.sleep(0)
        positives[t]=posCount
        negatives[t]=negCount



        if negCount>4 or posCount>4:
            if False:print (tweet,posCount,negCount)
    c+=1
    combined=np.vstack((positives,negatives,positives-negatives)).T


    np.savetxt('sentiments.txt',combined,fmt="%d",delimiter='\t')


    counts,xedges,yedges,im=plt.hist2d(positives,negatives,bins=[int(np.max(positives)),int(np.max(negatives))])
    print('tn',tn)
    print('fp', fp)
    print('tp',tp)
    print('fn', fn)
##    print '%2.2f HAVE ZERO SENTIMENT' % (100.0*counts[0,0]/len(positives))

##    if False:
##     Plot distribution of sentiments?
##    fig=plt.figure()
##    ax=fig.add_subplot(211)
##    posRange=range(0,int(np.max(positives))+1)
##    ax.hist(positives,bins=posRange)
##    plt.xticks([0.5+i for i in posRange],[str(i) for i in posRange])
##    plt.ylabel('Positive Sentiment')
##
##    ax=fig.add_subplot(212)
##    negRange=range(0,int(np.max(negatives))+1)
##    ax.hist(negatives,bins=negRange)
##    plt.xticks([0.5+i for i in negRange],[str(i) for i in negRange])
##    plt.ylabel('Negative Sentiment')
##    plt.show()

if __name__=="__main__":
  main()
