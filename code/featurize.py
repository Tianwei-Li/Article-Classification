#!/usr/bin/env python

import sys
from sets import Set

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
    stopword_file = open("stopwords.txt", 'r')
    content = stopword_file.read().strip()
    stop_words = content.split('\n')
    stopWordSet = Set(stop_words)

    # create dictionary
    wordDic = {}
    wordMatrix = []
    for article in train_articles:
        words = article.strip().split()
        words = filtStopWords(words, stopWordSet)
        wordMatrix.append(words)
        for word in words:
            if word not in wordDic:
                wordDic[word] = 0


    # generate word count for train articles
    trainFeatures = []
    for words in wordMatrix:
        for word in words:
            wordDic[word] += 1
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
                csvfile.write(', '.join([str(feature) for feature in row]))
                csvfile.write('\n')

if __name__ == '__main__':
    articles_to_features(*sys.argv[1:5])
