function [] = evaluate()
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here


c = classify_tfidf('train_feature.csv', '../data/labels_train.txt', 'test_feature.csv');
% c = classifyNB_Berno('train_feature.csv', '../data/labels_train.txt', 'test_feature.csv');

%c = classify_tfidf('./smallcase/train_feature.csv', './smallcase/train_label.txt', './smallcase/test_feature.csv');

yValid = csvread('../data/labels_valid.txt');
accurate = length(find((c-yValid)==0)) / length(c)
end

