function [c] = classify_tfidf(XTrain_fName, yTrain_fName, XTest_fName)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

% multinomial unigram language model

XTrain = csvread(XTrain_fName);
XTest = csvread(XTest_fName);
yTrain = csvread(yTrain_fName);


% get the prior probability for each class
probs = prior(yTrain);
nClass = size(probs, 1);

[scores] = tfidf(XTrain, yTrain, XTest, nClass);

% classify
nTest = size(XTest, 1);
c = zeros(nTest, 1);

for i = 1 : nTest
    bayes = zeros(1, nClass);
    for j = 1 : nClass
        bayes(j) = sum(XTest(i, :) .* log(scores(j,:))) + log(probs(j));
    end
    [maxP, idx] = max(bayes);
    c(i,1) = idx - 1;
    
end

end

function [scores] = tfidf(XTrain, yTrain, XTest, nClass)
% train the classifier

% idf (term) = log ( N * M_term / N_term )



[N, nFeat] = size(XTrain);

M_term = zeros(nClass, nFeat);
tf = zeros(nClass, nFeat);

XCount = XTrain > 0;
N_term = sum(XCount, 1);

for j = 0 : nClass-1
    % calculate the tf for each label
    [r, c] = find(yTrain == j);
    tempX = XTrain(r,:);
    tempXCount = XCount(r, :);
    
    M_term(j+1, :) = sum(tempXCount, 1);
    
    totalCnt = sum(tempX(:)) + nFeat;  % total word count, add 1 smooth
    tf(j+1, :) = sum(tempX, 1) + 1;
    tf(j+1, :) = tf(j+1, :) ./ totalCnt;
end

N_term = N_term + nClass;
M_term = M_term + 1;  % plus 1 smooth

scores = tf .* log(N * M_term ./ repmat(N_term, nClass, 1));


end


function [ probs ] = prior( y )

% get the prior probability for each class
% input y is the vector of the training labels
% output the probability of each class
[row, col] = size(y);
count = hist(y, unique(y));
probs = count.'/row;

end



