#!/usr/bin/env python

from __future__ import division, unicode_literals
import math
import sys
from sets import Set
from textblob import TextBlob as tb
#import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)
          
def idf(labellist, word, bloblist):
    return math.log(len(bloblist) * n_containing(word, labellist)  / (1 + n_containing(word, bloblist)))
              
def tfidf(labellist, word, blob, bloblist):
    return tf(word, blob) * idf(labellist, word, bloblist)

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
    

def test(train_data_name, train_label_name):
    with open(train_data_name, 'r') as in_file:
        train_data_lines = in_file.readlines()
    
    # Get the label list index of 0,1,2,3
    label_0_list, label_1_list, label_2_list, label_3_list = calculate_M(train_label_name)
    
    # generate the stop words hash set and delete stop words
    stopword_file = open("stopwords.txt", 'r')
    content = stopword_file.read().strip()
    stop_words = content.split('\n')
    stopWordSet = Set(stop_words)
    
    train_filter_data = []
    for article in train_data_lines:
        words = article.strip().split()
        words = filtStopWords(words, stopWordSet)
        train_filter_data.append(words)
        
    
   # with open(train_label_name, 'r') as in_file:
   #    train_label_lines = in_file.readlines()
    
    bloblist = []
    wholeblob = ""
    for item in train_filter_data:
        item = '  '.join(item)
        wholeblob = wholeblob + item 
        bloblist.append(tb(item))
    
    wholeblob = tb(wholeblob)
    
    bloblist_0 = [bloblist[i] for i in label_0_list]
    bloblist_1 = [bloblist[i] for i in label_1_list]
    bloblist_2 = [bloblist[i] for i in label_2_list]
    bloblist_3 = [bloblist[i] for i in label_3_list]
    
                         
    #bloblist = [document1, document2, document3]
    scores = {word: tfidf(bloblist_0, word, wholeblob, bloblist) for word in wholeblob}
    #sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse = True)
    for word, score in sorted_words[:100]:
        print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
    
            
if __name__ == '__main__':
    test(*sys.argv[1:3])
    
    
    
   # for i, blob in enumerate(bloblist):
    #    print("Top words in document {}".format(i + 1))                           
     #   scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
      #  sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
       # for word, score in sorted_words[:100]:
        #    print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
