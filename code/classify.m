function [c] = classify(XTrain_fName, yTrain_fName, XTest_fName)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

% multinomial unigram language model

XTrain = csvread(XTrain_fName);
XTest = csvread(XTest_fName);
yTrain = csvread(yTrain_fName);


% get the prior probability for each class
probs = prior(yTrain);
nClass = size(probs, 1);

[XTest, condProb] = train(XTrain, yTrain, XTest, nClass);

% classify
nTest = size(XTest, 1);
c = zeros(nTest, 1);

for i = 1 : nTest
    bayes = zeros(1, nClass);
    for j = 1 : nClass
        bayes(j) = sum(XTest(i, :) .* log(condProb(j,:))) + log(probs(j));
    end
    [maxP, idx] = max(bayes);
    c(i,1) = idx - 1;
    
end

end

function [XTest, condProb] = train(XTrain, yTrain, XTest, nClass)
% train the classifier
nFeat = size(XTrain, 2);
condProb = zeros(nClass, nFeat);
for j = 0 : nClass-1
    [r, c] = find(yTrain == j);
    tempX = XTrain(r,:);

    totalCnt = sum(tempX(:)) + nFeat;  % total word count, add 1 smooth
    condProb(j+1, :) = sum(tempX, 1) + 1;
    condProb(j+1, :) = condProb(j+1, :) ./ totalCnt;
end

 % remove noise features
 scales = floor(log10(condProb));
 % find max and min scales for each feature
 maxP = max(scales,[],1);
 minP = min(scales,[],1);
 [row, col] = find(maxP ~= minP);

%maxP = max(condProb,[],1);
%minP = min(condProb,[],1);
%[row, col] = find(maxP - minP > 0.001);

XTest = XTest(:, col);
condProb = condProb(:, col);
end


