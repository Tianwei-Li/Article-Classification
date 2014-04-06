#!/usr/bin/env python

from __future__ import division, unicode_literals
import math
import sys
from sets import Set
from textblob import TextBlob as tb
#import TextBlob as tb

def tf(worddic_label, label_blob, word):
    return worddic_label[word] / len(label_blob.words)

def n_containing(worddic, word):
    return worddic[word]
          
def idf(word, bloblist, worddic):
    return math.log(len(bloblist) / (1 + n_containing(worddic, word)))
              
def tfidf(label_blob, worddic_label, worddic, word, bloblist):
    return tf(worddic_label, label_blob, word) * idf(word, bloblist, worddic)

def filtStopWords(wordsOrg, stopWordSet):
    words = []
    for word in wordsOrg:
        if word not in stopWordSet:
            words.append(word)
    
    return words

def calculate_M(train_label_name):
    labels_file = open(train_label_name, 'r')
    content = labels_file.read()
    labels_list = content.split('\n')
    
    label_0_list = [i for i, x in enumerate(labels_list) if x == '0']
    label_1_list = [i for i, x in enumerate(labels_list) if x == '1']
    label_2_list = [i for i, x in enumerate(labels_list) if x == '2']
    label_3_list = [i for i, x in enumerate(labels_list) if x == '3']
    
    return (label_0_list, label_1_list, label_2_list, label_3_list)

def calculate_wordcount(worddic, train_filter_data):
    for line in train_filter_data:
        for word in line:
            worddic[word] = worddic[word] + 1   
    return worddic 
    
def generateTestFeature(test_data_name):
    
    with open(test_data_name, 'r') as infile:
        test_lines = infile.readlines()
    
    # generate the stop words hash set and delete stop words
    stopword_file = open("stopwords.txt", 'r')
    content = stopword_file.read().strip()
    stop_words = content.split('\n')
    stopWordSet = Set(stop_words)
    
    test_filter_data = []
    for i, article in enumerate(test_lines):
        words = article.strip().split()
        words = filtStopWords(words, stopWordSet)
        test_filter_data.append(words)
    
    return test_filter_data
        

def test(test_data_name, test_feature_name, train_data_name, train_label_name,label_0_score, label_1_score, label_2_score, label_3_score):
    with open(train_data_name, 'r') as in_file:
        train_data_lines = in_file.readlines()
    
    worddic = {}
    worddic_0 = {}
    worddic_1 = {}
    worddic_2 = {}
    worddic_3 = {}
    
    test_worddic = {}
    
    wordset = set()
    # Get the label list index of 0,1,2,3
    label_0_list, label_1_list, label_2_list, label_3_list = calculate_M(train_label_name)
    
    # generate the stop words hash set and delete stop words
    stopword_file = open("stopwords.txt", 'r')
    content = stopword_file.read().strip()
    stop_words = content.split('\n')
    stopWordSet = Set(stop_words)
    
    train_filter_data_0 = []
    train_filter_data_1 = []
    train_filter_data_2 = []
    train_filter_data_3 = []
    
    train_filter_data = []
    for i, article in enumerate(train_data_lines):
        words = article.strip().split()
        words = filtStopWords(words, stopWordSet)
        if i in label_0_list:
            train_filter_data_0.append(words)
        if i in label_1_list:
            train_filter_data_1.append(words)
        if i in label_2_list:
            train_filter_data_2.append(words)
        if i in label_3_list:
            train_filter_data_3.append(words)
            
        train_filter_data.append(words)
       
    # Add word to wordset 
    for item in train_filter_data:
        for word in item:
            wordset.add(word)
    
    for word in wordset:
        worddic[word] = 0
        worddic_0[word] = 0
        worddic_1[word] = 0
        worddic_2[word] = 0
        worddic_3[word] = 0
        
        test_worddic[word] = 0
    #=================================================================
    
    test_data = generateTestFeature(test_data_name)
    
    with open (test_feature_name, 'wb') as csvfile:
        
        for line in test_data:
            for word in line:
                if word in wordset:
                    test_worddic[word] += 1
        
        for word, count in test_worddic.items():
            csvfile.write(str(count) + " ")
        csvfile.write('\n')
        
        for word, count in test_worddic.items():
            test_worddic[word] = 0
    
    #==================================================================
    
    
    worddic = calculate_wordcount(worddic, train_filter_data)   
    worddic_0 = calculate_wordcount(worddic_0, train_filter_data_0) 
    worddic_1 = calculate_wordcount(worddic_1, train_filter_data_1) 
    worddic_2 = calculate_wordcount(worddic_2, train_filter_data_2) 
    worddic_3 = calculate_wordcount(worddic_3, train_filter_data_3) 
    #wordset.add('prefer')
    #wordset.add('sport')
    #wordset.add('now')         
   # with open(train_label_name, 'r') as in_file:
   #    train_label_lines = in_file.readlines()
    
    bloblist = []
    label_0_blob = ""
    label_1_blob = ""
    label_2_blob = ""
    label_3_blob = ""
    
    for i, item in enumerate(train_filter_data):
        item = '  '.join(item)
        if i in label_0_list:
            label_0_blob = label_0_blob + item + " "
        if i in label_1_list:
            label_1_blob = label_1_blob + item + " "
        if i in label_2_list:
            label_2_blob = label_2_blob + item + " "
        if i in label_3_list:
            label_3_blob = label_3_blob + item + " "
        bloblist.append(tb(item))
    
    label_0_blob = tb(label_0_blob)
    label_1_blob = tb(label_1_blob)
    label_2_blob = tb(label_2_blob)
    label_3_blob = tb(label_3_blob)
    
    bloblist_0 = [bloblist[j] for j in label_0_list]
    bloblist_1 = [bloblist[j] for j in label_1_list]
    bloblist_2 = [bloblist[j] for j in label_2_list]
    bloblist_3 = [bloblist[j] for j in label_3_list]
      
                         
    #bloblist = [document1, document2, document3]  label_blob, worddic_label, worddic, word, bloblist
    scores_0 = {word: tfidf(label_0_blob, worddic_0, worddic, word, bloblist) for word in wordset}
    scores_1 = {word: tfidf(label_1_blob, worddic_1, worddic, word, bloblist) for word in wordset}
    scores_2 = {word: tfidf(label_2_blob, worddic_2, worddic, word, bloblist) for word in wordset}
    scores_3 = {word: tfidf(label_3_blob, worddic_3, worddic, word, bloblist) for word in wordset}
    
    sorted_words_0 = sorted(scores_0.items(), key=lambda x: x[1], reverse = True)
    sorted_words_1 = sorted(scores_1.items(), key=lambda x: x[1], reverse = True)
    sorted_words_2 = sorted(scores_2.items(), key=lambda x: x[1], reverse = True)
    sorted_words_3 = sorted(scores_3.items(), key=lambda x: x[1], reverse = True)
    
    with open(label_0_score, 'wb') as csvfile:
        for word, score in scores_0.items():
            csvfile.write(str(score) + " ")
            #print("Word: {}, TF-IDF: {}".format(word, round(score, 10)))
    with open(label_1_score, 'wb') as csvfile:
        for word, score in scores_0.items():
            csvfile.write(str(score) + " ")
            
    with open(label_2_score, 'wb') as csvfile:
        for word, score in scores_0.items():
            csvfile.write(str(score) + " ")
            
    with open(label_3_score, 'wb') as csvfile:
        for word, score in scores_0.items():
            csvfile.write(str(score) + " ")
    
    
            
if __name__ == '__main__':
    test(*sys.argv[1:9])
    
    
    
   # for i, blob in enumerate(bloblist):
    #    print("Top words in document {}".format(i + 1))                           
     #   scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
      #  sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
       # for word, score in sorted_words[:100]:
        #    print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
