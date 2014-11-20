
# coding: utf-8

# In[117]:

def test_bfl(wrapletter,word):
    #determines number of characters left/up relative to wrapletter
    #assumes capital letter indicates wrapletter in lowercase word and is in word
    basenum=0
    for i in word:
        if i==wrapletter:
            return(basenum)
        else:
            basenum=basenum+1

def test_afl(wrapletter,word):
    #determines number of characters right/down relative to wrapletter;
    #assumes capital letter indicates wrapletter in lowercase word and is in word
    basenum=0
    for i in word[::-1]:
        if i==wrapletter:
            return(basenum)
        else:
            basenum=basenum+1

def letter_placement(letterscoreplacement,wrapletter,word):
    #determines what letter is in letterscoreplacement#
    L,afl=list(word),test_afl(wrapletter,word)
    return(L[len(word)-afl-1-letterscoreplacement])
    
def all_variants(wrapletter,word):
    #indicates location of wrapletter in word with capital letter;
    #i.e., given 't' and 'tattle', returns [Tattle,taTtle,tatTle]
    L=[]
    for i in range(len(word)):
        if(word[i]==wrapletter):
            L.append(word[0:i].lower()+word[i].upper()+word[i+1::].lower())
    return(L)

def ScrabbleHelperBaseF(wrapletter,letters,beforewrapletter=15,afterwrapletter=15,wordscoremod=[1],wordscoreplacement=[0],letterscoremod=[1],letterscoreplacement=[0]):
    #Is base function for ScrabbleHelper
    #OSPD is the official scrabble word list#
    #afterletter and beforeletter are int referencing spaces available
    #on board relative to wrapletter (up/left for before, down/right for after)#
    #wordscoremod is the Word Score Modifier (Triple or Double), if it exists#
    #wordscoreplacement is placement of mod tile relative to wrapletter (positive is up/left;
    #negative is down/right) expressed as int number of spaces#
    #letterscoremod/placement works same as with word, but only for a particular letter,
    #and LSP/LSM is a list, in case of multiple LSM spaces#
    #Blank indicates presense of blank tile in letters.  Currently assumes that blanks still have a points value#
    scrabdict,WLU={'a':1,'b':3,'c':3,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':8,'k':5,'l':1,'m':3,'n':1,'o':1,'p':3,
               'q':10,'r':1,'s':1,'t':1,'u':1,'v':4,'w':4,'x':8,'y':4,'z':10,'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,
               'G':2,'H':4,'I':1,'J':8,'K':5,'L':1,'M':3,'N':1,'O':1,'P':3,'Q':10,'R':1,'S':1,'T':1,'U':1,
               'V':4,'W':4,'X':8,'Y':4,'Z':10,'_':0},wrapletter.upper()
    sfile,hitlistd,wordlistd=open('ospd.txt'),{},{}
    lettersL=list(letters+WLU)
    for line in sfile:
        baseword=line.strip()
        #checks wrapletter in word and word length#
        if wrapletter in baseword and len(baseword)<=len(lettersL):
            #checks each variant of the word depending on wrapletter placement#
            for i in all_variants(wrapletter,baseword):
                #checks AFL/BFL#
                if test_bfl(WLU,i)<=beforewrapletter and test_afl(WLU,i)<=afterwrapletter:
                    for char in i:
                        #checks all char in word are also in lettersL + number of chars <= number of chars 
                        #in lettersL; if not, adds to hitlist for later termination#
                        if char in lettersL and lettersL.count(char)>=list(i).count(char):
                            pass
                        else:
                            basenum=0
                            for let in i:
                                basenum=basenum+scrabdict[let]
                            hitlistd[i]=basenum
                            break
                        #creates score associated with word in dictionary#
                        basenum=0
                        for let in i:
                            basenum=basenum+scrabdict[let]
                    #Double/Triple Letter Modifier#
                    if len(letterscoreplacement)>1:
                        for num in range(len(letterscoreplacement)):
                            if letterscoreplacement[num]==0:
                                basenum=basenum+scrabdict[WLU]*(letterscoremod[num]-1)
                            #test that word lands on letter modifier
                            elif letterscoreplacement[num]>0 and letterscoreplacement[num]>test_bfl(WLU,i):
                                pass
                            elif letterscoreplacement[num]<0 and letterscoreplacement[num]*-1>test_afl(WLU,i):
                                pass
                            else:
                                basenum=basenum+scrabdict[letter_placement(letterscoreplacement[num],WLU,i)]*(letterscoremod[num]-1)
                    elif len(letterscoreplacement)==1:
                        if letterscoreplacement[0]==0:
                            basenum=basenum+scrabdict[WLU]*(letterscoremod[0]-1)
                        #test that word lands on letter modifier
                        elif letterscoreplacement[0]>0 and letterscoreplacement[0]>test_bfl(WLU,i):
                            pass
                        elif letterscoreplacement[0]<0 and letterscoreplacement[0]*-1>test_afl(WLU,i):
                            pass
                        else:
                            basenum=basenum+scrabdict[letter_placement(letterscoreplacement[0],WLU,i)]*(letterscoremod[0]-1)
                    else:
                        pass
                    #Double/Triple/Quadruple/6tuple/9tuple word modifier#
                    for num in range(len(wordscoreplacement)):
                        if wordscoreplacement[num]>=0 and test_bfl(WLU,i)>=wordscoreplacement[num]:
                            basenum=basenum*wordscoremod[num]
                        elif wordscoreplacement[num]<=0 and test_afl(WLU,i)<=(wordscoreplacement[num]*-1):
                            basenum=basenum*wordscoremod[num]
                        else:
                            pass
                    #50 point bonus if all letters used#
                    if len(i)==len(lettersL) and list(sorted(i))==sorted(lettersL) and len(i)==8:
                        basenum=basenum+50
                    #word:score#
                    wordlistd[i]=basenum
                else:
                    pass
        else:
            pass
    #termination script#
    for word in hitlistd:
        if word in wordlistd:
            del wordlistd[word]
    sfile.close()
    #determining best word; returns result in dictionary with key=int score#
    topplay,topscore=[],0
    for word in wordlistd.keys():
        if wordlistd[word]==topscore:
            topplay.append(word)
        elif wordlistd[word]<topscore:
            pass
        else:
            topplay=[]
            topscore=wordlistd[word]
            topplay.append(word)
    return((topplay,topscore))

def ScrabbleHelperV4(wrapletters,letters,BWL=[15],AWL=[15],WSM=[[1]],WSP=[[0]],LSM=[[1]],LSP=[[0]],blank=False):
    #creates for loop to run SHBF with multiple wrapletters and associated LSPs/LSMs/WSMs/WSPs
    #and picks out best word given wrapletters#
    #note that LSP/LSM/WSP/WSM must be entered as multiple lists to go with multiple wrapletters#
    #arconyms refer to inputs of SHBF#
    topwordsd,bestplay,bestscore,all_letters={},[],0,'abcdefghijklmnopqrstuvwxyz'
    #creates dictionary containing words and their associated scores#
    if blank is False:
        for i in range(len(wrapletters)):
            topwordsd[tuple(ScrabbleHelperBaseF(wrapletters[i],letters,BWL[i],AWL[i],WSM[i],WSP[i],LSM[i],LSP[i])[0])]=ScrabbleHelperBaseF(wrapletters[i],letters,BWL[i],AWL[i],WSM[i],WSP[i],LSM[i],LSP[i])[1]
    else:
        for i in all_letters:
            lettersB=letters+i
            for i in range(len(wrapletters)):
                topwordsd[tuple(ScrabbleHelperBaseF(wrapletters[i],lettersB,BWL[i],AWL[i],WSM[i],WSP[i],LSM[i],LSP[i])[0])]=ScrabbleHelperBaseF(wrapletters[i],lettersB,BWL[i],AWL[i],WSM[i],WSP[i],LSM[i],LSP[i])[1]
            lettersB=''
    #looks through aforementioned dictionary for best word based on score#
    for word in topwordsd.keys():
        if topwordsd[word]==bestscore:
            bestplay.append(word)
        elif topwordsd[word]<bestscore:
            pass
        else:
            bestplay=[]
            bestscore=topwordsd[word]
            bestplay.append(word)
    bestplay.append(bestscore)
    bestplay.reverse()
    return(bestplay)


# In[127]:

import time
TL=0
n=10
for number in range(n):
    x=time.time()
    print(ScrabbleHelperV4('a','hfibegyt'))
    y=time.time()
    print(y-x)
    TL=TL+(y-x)
print('Average time is:',TL/n,'seconds')


# In[ ]:



