
 
def test_bfl(wrapletter,word):
    d={}
    basenum=0
    for i in word:
        if i in d.keys():
            pass
        else:
            d[i]=basenum
            basenum=basenum+1
    return(d[wrapletter])
 
def test_afl(wrapletter,word):
    d={}
    basenum=0
    for i in word:
        if i in d.keys():
            pass
        else:
            d[i]=basenum
            basenum=basenum+1
    return(basenum-d[wrapletter])
 
def ScrabbleHelper(wrapletter,letters,afterwrapletter=10,beforewrapletter=10):
    #OSPD is the official scrabble word list
    #afterletter and beforeletter are int referencing spaces available
    #on board relative to wrapletter (up/left for before, down/right for after)
    sfile=open('ospd.txt')
    lettersL=list(letters+wrapletter)
    scrabdict={'a':1,'b':3,'c':3,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':8,'k':5,'l':1,'m':3,'n':1,'o':1,'p':3,'q':10,'r':1,'s':1,'t':1,'u':1,'v':4,'w':4,'x':8,'y':4,'z':10}
    hitlistd={}
    wordlistd={}
    #analyzes each word in OSPD
    for line in sfile:
        i=line.strip()
        #checks word length, AFL/BFL, and presense of wrapletter
        if wrapletter in i and len(i)<=len(lettersL) and test_bfl(wrapletter,i)<=beforewrapletter and test_afl(wrapletter,i)<=afterwrapletter:
            for char in i:
                #checks all char in word are also in lettersL + number of chars <= number of chars
                #in lettersL; if not, adds to hitlist for later termination
                if char in lettersL and lettersL.count(char)>=list(i).count(char):
                    pass
                else:
                    basenum=0
                    for let in i:
                        basenum=basenum+scrabdict[let]
                    hitlistd[i]=basenum
                    break
                #creates score associated with word in dictionary
                basenum=0
                for let in i:
                    basenum=basenum+scrabdict[let]
                wordlistd[i]=basenum
        else:
            pass
    #termination script
    for word in hitlistd:
        if word in wordlistd:
            del wordlistd[word]
    #determining best word; returns result in list with int score
    bestplay=[]
    bestscore=0
    for word in wordlistd.keys():
        if wordlistd[word]==bestscore:
            bestplay.append(word)
        elif wordlistd[word]<bestscore:
            pass
        else:
            bestplay=[]
            bestplay.append(word)
            bestscore=wordlistd[word]
    print('Given a wrapletter of "',wrapletter,'", the following words yield a highest score of:',bestscore)
    return(bestplay)
 
 
 
import time
x=time.time()
stuff='oayvilse'
for i in stuff:
    print(ScrabbleHelper(i,'ghniiuy'))
y=time.time()
print(y-x)
 
 
# In[ ]:
 
#blanks = 0 points
#no backwards words
