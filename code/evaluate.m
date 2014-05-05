function [] = evaluate()
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here


%c = classify_tfidf('train_wordcnt.csv', '../data/labels_train.txt', 'test_wordcnt.csv');

c = classify_tfidf('train_stem_wordcnt.csv', '../data/labels_train.txt', 'test_stem_wordcnt.csv');

% c = classify('train_wordcnt.csv', '../data/labels_train.txt', 'test_wordcnt.csv');

% c = classify_TCNB('train_wordcnt.csv', '../data/labels_train.txt', 'test_wordcnt.csv');
% c = classify_pca('train_wordcnt.csv', '../data/labels_train.txt', 'test_wordcnt.csv');

% c = classify_tfidf('./smallcase/train_feature.csv', './smallcase/train_label.txt', './smallcase/test_feature.csv');

yValid = csvread('../data/labels_valid.txt');
accurate = length(find((c-yValid)==0)) / length(c)
end

