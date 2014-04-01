# An implementation of the Porter Stemming Algorithm
# (c) scott a kaplan
# This is a python implementation of a commonly used stemming algorithm.  This algorithm strips
# of suffixes from words so words with common stems can be indexed in common areas.  Most of the
# documentation of the algorithm was obtained from Porter's original paper which can be found at
# http://www.muscat.co.uk/~martin/stem.html.  Similar implementations can be found at that same
# website.  There is also a version called Perl::Text, but it deviates in a number of places from the 
# original algrorithm.  This implementation is pretty much equivalent to the implementation of the
# algorithms on that web page.  Originally I had the whole thing coded with regular expressions
# but it was very slow. I removed as many of of the regular expressions as I could, and it
# increased the performance about 7 times.  I hope this is useful to someome, and welcome suggestions at
# skaplan@wso.williams.edu
# All of these ideas are from or derived from the algorithms at http://www.muscat.co.uk/~martin/stem.htm


## TODO:
## make faster ?? port to a C module??
## do i need to check more boundary conditions on the words (i.e. indexErrors)

import re
from sets import Set 
import sys
from string import lower



#used in all steps
_c =    "[^aeiou]"          # consonant
_v =    "[aeiouy]"          # vowel
_C =    _c + "[^aeiouy]*"    # consonant sequence
_V =    _v + "[aeiou]*"      # vowel sequence

Mgre0 = re.compile("^(" + _C + ")?" + _V + _C)               # [C]VC... is m>0
Meq1 = re.compile("^(" + _C + ")?" + _V + _C +"(" + _V + ")"+ "?" + "$")  # [C]VC[V] is m=1
Mgre1 = re.compile("^(" + _C + ")?" + _V + _C + _V + _C)        # [C]VCVC... is m>1
CVCending = re.compile(_C + _v + "[^aeiouwxy]$")
vstem   = re.compile("^(" + _C + ")?" + _v)                   # vowel in stem
DoubleConsonant=  re.compile(r"([^aeiouylsz])\1$")   #matches double consonants excpet l s and z
removeEndingPunc  =  re.compile(r"[^a-z]+$")


def stem(parms):
    stems = []
    for word in parms:

        ######## step 0               pre-process words
        word = lower(word)
        word = re.sub(removeEndingPunc,"",word)
        if word[-2:] == "'s": word = word[:-2]  #remove newlines if taken from a file
        

        if len(word) < 3:            #don't stem if word smaller than 3  
            stems.append(word)      
            continue

        if word[0] == 'y': word = 'Y' + word[1:]      #make sure initial Y is not considered a vowel

        
        ##Step 1a
        ## SSES -> SS                         caresses  ->  caress
        ## IES  -> I                          ponies    ->  poni
        ##                                    ties      ->  ti
        ## SS   -> SS                         caress    ->  caress
        ## S    ->                            cats      ->  cat
        ## this could be better even if the match string is not in the target string
        ## sub still returns a string, so i have to check twice, is there a better way to do this

        if word[-1] == 's' and word[-2] != 's':
            if word[-4:] == 'sses':
                word = word[:-4] + 'ss'
            elif word[-3:] == 'ies':
                word = word[:-3] +  'i'
            else:
                word = word[:-1]


        ## Step 1b

        ##     (m>0) EED -> E                     feed      ->  feed ??? huh m is < 0
        ##                                        agreed    ->  agree
        ##     (*v*) ED  ->                       plastered ->  plaster
        ##                                        bled      ->  bled
        ##     (*v*) ING ->                       motoring  ->  motor
        ##                                        sing      ->  sing
       

        ## The rule to map to a single letter causes the removal of one of the double
        ## letter pair. The -E is put back on -AT, -BL and -IZ, so that the suffixes
        ## -ATE, -BLE and -IZE can be recognised later. This E may be removed in step
        ## 4.

        flag = None                         #only set to 1 2nd and 3rd steps are taken
        if word[-3:] == 'eed':                    # m>0   eed -> ee
            if Mgre0.search(word[:-3]):
                word = word[:-3] + "ee"

        elif word[-2:] == 'ed':                   # *v* ed
            if vstem.search(word[:-2]):
                word = word[:-2]
                flag = 1
        elif word[-3:] == 'ing':                  # *v* ing
            if vstem.search(word[:-3]):
                word = word[:-3]
                flag = 1


        # step 1b1
        ## If the second or third of the rules in Step 1b is successful, the following
        ## is done:

        ##     AT -> ATE                       conflat(ed)  ->  conflate
        ##     BL -> BLE                       troubl(ed)   ->  trouble
        ##     IZ -> IZE                       siz(ed)      ->  size
        ##     (*d and not (*L or *S or *Z))
        ##        -> single letter
        ##                                     hopp(ing)    ->  hop
        ##                                     tann(ed)     ->  tan
        ##                                     fall(ing)    ->  fall
        ##                                     hiss(ing)    ->  hiss
        ##                                     fizz(ed)     ->  fizz
        ##     (m=1 and *o) -> E               fail(ing)    ->  fail
        ##                                     fil(ing)     ->  file


        if flag:                                                # go on to part 1b2
            if word[-2:] == 'at':                               # at -> ate
                word = word[:-2] + 'ate' 
            elif word[-2:] == 'bl':                             # bl -> ble 
                word = word[:-2] + 'ble' 
            elif word[-2:] == 'iz':                             # iz -> ize   
                word = word[:-2] + 'ize' 
            elif DoubleConsonant.search(word):                  # the word (so far) ends in a double consonant except
                word = word[:-1]                                # for l , s and z, replace with single consonant
            elif CVCending.search(word) and Meq1.search(word):  # m= 1 and word ends in CVC sequence
                word = word + 'e'                               # add an e



        #step 1c
        # (*v*) Y -> I                    happy        ->  happi
        #                                 sky          ->  sky

        if word[-1:] == 'y':                    ##change to [-1]
            if vstem.search(word[:-1]):
                word = word[:-1] + 'i'                    






        ##  Step 2

        ##     (m>0) ATIONAL ->  ATE           relational     ->  relate
        ##     (m>0) TIONAL  ->  TION          conditional    ->  condition
        ##                                     rational       ->  rational
        ##     (m>0) ENCI    ->  ENCE          valenci        ->  valence
        ##     (m>0) ANCI    ->  ANCE          hesitanci      ->  hesitance
        ##     (m>0) IZER    ->  IZE           digitizer      ->  digitize
        ##     (m>0) ABLI    ->  ABLE          conformabli    ->  conformable
        ##     (m>0) ALLI    ->  AL            radicalli      ->  radical
        ##     (m>0) ENTLI   ->  ENT           differentli    ->  different
        ##     (m>0) ELI     ->  E             vileli        - >  vile
        ##     (m>0) OUSLI   ->  OUS           analogousli    ->  analogous
        ##     (m>0) IZATION ->  IZE           vietnamization ->  vietnamize
        ##     (m>0) ATION   ->  ATE           predication    ->  predicate
        ##     (m>0) ATOR    ->  ATE           operator       ->  operate
        ##     (m>0) ALISM   ->  AL            feudalism      ->  feudal
        ##     (m>0) IVENESS ->  IVE           decisiveness   ->  decisive
        ##     (m>0) FULNESS ->  FUL           hopefulness    ->  hopeful
        ##     (m>0) OUSNESS ->  OUS           callousness    ->  callous
        ##     (m>0) ALITI   ->  AL            formaliti      ->  formal
        ##     (m>0) IVITI   ->  IVE           sensitiviti    ->  sensitive
        ##     (m>0) BILITI  ->  BLE           sensibiliti    ->  sensible


        # in addition
        ##     (m>0) LOGI    -> LOG
        
        
        index = word[-2]
        if index == 'a':
            if word[-7:] == 'ational' :
                if Mgre0.search(word[:-7]): word = word[:-7] + 'ate'
            elif word[-6:] == 'tional' :
                if Mgre0.search(word[:-6]): word = word[:-6] + 'tion'
        elif index  == 'c':
            if word[-4:] == 'enci' :
                if Mgre0.search(word[:-4]) : word = word[:-4] + 'ence'
            elif word[-4:] == 'anci' :
                if Mgre0.search(word[:-4]) : word = word[:-4] + 'ance'
        elif index  == 'e':
            if word[-4:] == 'izer' :
                if Mgre0.search(word[:-4]) : word = word[:-4] + 'ize'
        elif index  == 'l':
            if word[-3:] == 'bli':
                if Mgre0.search(word[:-3]): word = word[:-3] + 'ble' 
            elif word[-4:] == 'alli':
                if Mgre0.search(word[:-4]): word = word[:-4] + 'al'
            elif word[-5:] == 'entli':
                if Mgre0.search(word[:-5]): word = word[:-5] + 'ent'
            elif word[-3:] == 'eli':
                if Mgre0.search(word[:-3]): word = word[:-3] + 'e'
            elif word[-5:] == 'ousli':
                if Mgre0.search(word[:-5]): word = word[:-5] + 'ous'
        elif index  == 'o':
            if word[-7:] == 'ization':
                if Mgre0.search(word[:-7]): word = word[:-7] + 'ize' 
            elif word[-5:] == 'ation':
                if Mgre0.search(word[:-5]): word = word[:-5] + 'ate'
            elif word[-4:] == 'ator':
                if Mgre0.search(word[:-4]): word = word[:-4] + 'ate'
        elif index  == 's':
            if word[-5:] == 'alism':
                if Mgre0.search(word[:-5]): word = word[:-5] + 'al' 
            elif word[-7:] == 'iveness':
                if Mgre0.search(word[:-7]): word = word[:-7] + 'ive'
            elif word[-7:] == 'fulness':
                if Mgre0.search(word[:-7]): word = word[:-7] + 'ful'
            elif word[-7:] == 'ousness':
                if Mgre0.search(word[:-7]): word = word[:-7] + 'ous'
        elif index  == 't':
            if word[-5:] == 'aliti':
                if Mgre0.search(word[:-5]): word = word[:-5] + 'al' 
            elif word[-5:] == 'iviti':
                if Mgre0.search(word[:-5]): word = word[:-5] + 'ive'
            elif word[-6:] == 'biliti':
                if Mgre0.search(word[:-6]): word = word[:-6] + 'ble'
        elif index  == 'g':
            if word[-4:] == 'logi':
                if Mgre0.search(word[:-4]): word = word[:-4] + 'log' 
                

        ##    Step 3

        ##     (m>0) ICATE ->  IC              triplicate     ->  triplic
        ##     (m>0) ATIVE ->                  formative      ->  form
        ##     (m>0) ALIZE ->  AL              formalize      ->  formal 
        ##     (m>0) ICITI ->  IC              electriciti    ->  electric
        ##     (m>0) ICAL  ->  IC              electrical     ->  electric
        ##     (m>0) FUL   ->                  hopeful        ->  hope
        ##     (m>0) NESS  ->                  goodness       ->  good

        index = word[-1]
        if index == 'e':
            if word[-5:] == 'icate' :
                if Mgre0.search(word[:-5]): word = word[:-5] + 'ic'
            elif word[-5:] == 'ative' :
                if Mgre0.search(word[:-5]): word = word[:-5]
            elif word[-5:] == 'alize' :
                if Mgre0.search(word[:-5]): word = word[:-5] + 'al' 
        elif index  == 'i':
            if word[-5:] == 'iciti' :
                if Mgre0.search(word[:-5]) : word = word[:-5] + 'ic'
        elif index  == 'l':
            if word[-4:] == 'ical' :
                if Mgre0.search(word[:-4]) : word = word[:-4] + 'ic'
            if word[-3:] == 'ful' :
                if Mgre0.search(word[:-3]) : word = word[:-3] 
        elif index  == 's':
            if word[-4:] == 'ness' :
                if Mgre0.search(word[:-4]) : word = word[:-4] 


        ##         Step 4

        ##     (m>1) AL    ->                  revival        ->  reviv
        ##     (m>1) ANCE  ->                  allowance      ->  allow
        ##     (m>1) ENCE  ->                  inference      ->  infer
        ##     (m>1) ER    ->                  airliner       ->  airlin
        ##     (m>1) IC    ->                  gyroscopic     ->  gyroscop
        ##     (m>1) ABLE  ->                  adjustable     ->  adjust
        ##     (m>1) IBLE  ->                  defensible     ->  defens
        ##     (m>1) ANT   ->                  irritant       ->  irrit
        ##     (m>1) EMENT ->                  replacement    ->  replac
        ##     (m>1) MENT  ->                  adjustment     ->  adjust
        ##     (m>1) ENT   ->                  dependent      ->  depend
        ##     (m>1 and (*S or *T)) ION ->     adoption       ->  adopt
        ##     (m>1) OU    ->                  homologou      ->  homolog
        ##     (m>1) ISM   ->                  communism      ->  commun
        ##     (m>1) ATE   ->                  activate       ->  activ
        ##     (m>1) ITI   ->                  angulariti     ->  angular
        ##     (m>1) OUS   ->                  homologous     ->  homolog
        ##     (m>1) IVE   ->                  effective      ->  effect
        ##     (m>1) IZE   ->                  bowdlerize     ->  bowdler



        index = word[-2]
        if index == 'a':
            if word[-2:] == 'al' :
                if Mgre1.search(word[:-2]): word = word[:-2] 
        elif index  == 'c':
            if word[-4:] == 'ance' :
                if Mgre1.search(word[:-4]) : word = word[:-4]
            elif word[-4:] == 'ence' :
                if Mgre1.search(word[:-4]) : word = word[:-4]
        elif index  == 'e':
            if word[-2:] == 'er' :
                if Mgre1.search(word[:-2]) : word = word[:-2]
        elif index  == 'i':
            if word[-2:] == 'ic' :
                if Mgre1.search(word[:-2]) : word = word[:-2]
        elif index  == 'l':
            if word[-4:] == 'able':
                if Mgre1.search(word[:-4]): word = word[:-4]
            elif word[-4:] == 'ible':
                if Mgre1.search(word[:-4]): word = word[:-4]
        elif index  == 'n':
            if word[-3:] == 'ant':
                if Mgre1.search(word[:-3]): word = word[:-3]
            elif word[-5:] == 'ement':
                if Mgre1.search(word[:-5]): word = word[:-5]
            if word[-4:] == 'ment':
                if Mgre1.search(word[:-4]): word = word[:-4]
            elif word[-3:] == 'ent':
                if Mgre1.search(word[:-3]): word = word[:-3]
        elif index  == 'o':
            if word[-3:] == 'ion':
                try:
                    if word[-4] == 's' or word[-4]=='t':
                        if Mgre1.search(word[:-3]): word = word[:-3]
                except IndexError:pass
            elif word[-2:] == 'ou':
                if Mgre1.search(word[:-2]): word = word[:-2]
        elif index  == 's':
            if word[-3:] == 'ism':
                if Mgre1.search(word[:-3]): word = word[:-3]
        elif index  == 't':
            if word[-3:] == 'ate':
                if Mgre1.search(word[:-3]): word = word[:-3]
            elif word[-3:] == 'iti':
                if Mgre1.search(word[:-3]): word = word[:-3]
        elif index  == 'u':
            if word[-3:] == 'ous':
                if Mgre1.search(word[:-3]): word = word[:-3]
        elif index  == 'v':
            if word[-3:] == 'ive':
                if Mgre1.search(word[:-3]): word = word[:-3]
        elif index  == 'z':
            if word[-3:] == 'ize':
                if Mgre1.search(word[:-3]): word = word[:-3] 
                



     
        ##         Step 5a

        ##     (m>1) E     ->                  probate        ->  probat
        ##                                     rate           ->  rate
        ##     (m=1 and not *o) E ->           cease          ->  ceas

        ## Step 5b
        ##     (m > 1 and *d and *L) -> single letter
        ##                                     controll       ->  control
        ##                                     roll           ->  roll

        if word[-1:] == 'e':
        
            if Mgre1.search(word[:-1]):
                word = word[:-1]
            elif (Meq1.search(word[:-1])) and (not CVCending.search(word[:-1])):
                word = word[:-1]
                
        #step 5b
        if word[-2:] == 'll':
            if Mgre1.search(word):
                word = word[:-1]



        #clean up starting Y's
        if word[0] == 'Y': word = 'y' + word[1:]
        
        stems.append(word)      

    return stems

def filtStopWords(wordsOrg, stopWordSet):
    words = []
    for word in wordsOrg:
        if word not in stopWordSet:
            words.append(word)
    
    return words

def stemmingDocument(train_data_name, data_out_name):
    wordset = Set()
    with open(train_data_name, 'r') as in_file:
        document_lines = in_file.readlines()
    
    # generate the stop words hash set and delete stop words
    stopword_file = open("stopwords.txt", 'r')
    content = stopword_file.read().strip()
    stop_words = content.split('\n')
    stopWordSet = Set(stop_words)
    
    train_filter_data = []
    for article in document_lines:
        words = article.strip().split()
        words = filtStopWords(words, stopWordSet)
        train_filter_data.append(words)
    
    with open(data_out_name, 'wb') as out_file:
        for document_line in train_filter_data:
            #document_list = document_line.split(' ')
            stem_document = stem(document_line)
            for word in stem_document:
                wordset.add(word)
            string_document = ' '.join(stem_document)
            
            out_file.write("%s\n" % string_document)
    print len(wordset)
        
if __name__ == '__main__':
    stemmingDocument(*sys.argv[1:3])








