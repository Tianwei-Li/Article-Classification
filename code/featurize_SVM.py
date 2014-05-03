#!/usr/bin/env python

from __future__ import division, unicode_literals
import sys
from sets import Set
from collections import OrderedDict

def filtStopWords(wordsOrg, stopWordSet):
    words = []
    for word in wordsOrg:
        if word not in stopWordSet:
            words.append(word)
    
    return words


def featurize(train_articles, test_articles):
    '''
    Returns a tuple (train_features, test_features) of matrices of
    features. Each matrix is list of feature vectors, where a feature vector is
    simply a list of numbers. Note that features must be converted here to the
    proper numerical type (e.g., booleans should be converted to integers).
        
    You may find that returning a list of feature vectors is too
    memory-intensive. You can reduce memory usage considerably by defining the
    matrix as a Python generator that yields feature vectors, instead of
    building the whole list of vectors. For example, if your matrix was defined
    as [make_features(article) for article in articles], you could instead write
    (make_features(article) for article in articles). See
    https://wiki.python.org/moin/Generators for more details on
    generators. (Note that this approach may increase running time.)

    If you would like to examine an actual instance of the return type, try
    running the following function call using the default implementation:
       featurize(['train 1', 'training article 2'], ['test 1', 'the second test article'])
    and inspecting the return value.
    '''

    # generate the stop words hash set
    #stopword_file = open("stopwords.txt", 'r')
    #content = stopword_file.read().strip()
    #stop_words = content.split('\n')
    stop_words = ["a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","n't","'s","'d","'ll","'m","'ve","'re"]
    stopWordSet = Set(stop_words)

    # create dictionary
    wordDic1 = {}
    wordMatrix = []
    for article in train_articles:
        words = article.strip().split()
        words = filtStopWords(words, stopWordSet)
        wordMatrix.append(words)
        for word in words:
            if word not in wordDic1:
                wordDic1[word] = 1
            else:
                wordDic1[word] += 1


    # feature reduction, based on the frequency of words
    wordDic1 = sorted(wordDic1.items(), key=lambda t: t[1], reverse = True)
    wordDicLen = len(wordDic1)
    wordDic = {}
    idx = 0
    for item in wordDic1:
        wordDic[item[0]] = 0
        idx += 1
        if idx == wordDicLen:
            break
    

    # generate word count for train articles
    trainFeatures = []
    for words in wordMatrix:
        for word in words:
            if word in wordDic: wordDic[word] += 1
        trainFeatures.append(wordDic.values())
        # clear the dictionary
        for k in wordDic.keys() : wordDic[k] = 0
    
    
    # generate word count for test articles
    testFeatures = []
    for article in test_articles:
        words = article.strip().split()
        words = filtStopWords(words, stopWordSet)
        for word in words:
            if word in wordDic: wordDic[word] += 1
        testFeatures.append(wordDic.values())
        # clear the dictionary
        for k in wordDic.keys() : wordDic[k] = 0
        
    return (trainFeatures, testFeatures)




    ### REPLACE THE REST OF THIS FUNCTION WITH YOUR FEATURE GENERATION CODE ###
#    def make_features(articles):
#        return [[len(article.split()), int(article.startswith('the'))] for article in articles]
#    return (make_features(train_articles), make_features(test_articles))

def articles_to_features(train_in_name, train_out_name, test_in_name, test_out_name):
    
    with open(train_in_name, 'r') as in_file:
        train_lines = in_file.readlines()
    with open(test_in_name, 'r') as in_file:
        test_lines = in_file.readlines()

    train_features, test_features = featurize(train_lines, test_lines)

    for features, out_name in ((train_features, train_out_name),
                               (test_features, test_out_name)):
        with open(out_name, 'wb') as csvfile:
            # Output features in MATLAB-readable CSV format
            for row in features:
                idx = 1
                for feature in row:
                    csvfile.write(str(idx) + ":" + str(feature) + " ")
                    idx = idx + 1
                csvfile.write('\n')

if __name__ == '__main__':
    articles_to_features(*sys.argv[1:5])
