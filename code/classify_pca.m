function [c] = classify_pca(XTrain_fName, yTrain_fName, XTest_fName)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

% multinomial unigram language model

XTrain = csvread(XTrain_fName);
XTest = csvread(XTest_fName);
yTrain = csvread(yTrain_fName);

%test_train_inst = rand(5, 10);
%test_train_label = [1;1;1;-1;-1];
%model = svmtrain(test_train_label, test_train_inst, '-c 1 -g 0.07');
%[predict_label, accuracy, dec_values] = svmpredict(test_train_label, test_train_inst, model);


% get the prior probability for each class
probs = prior(yTrain);
nClass = size(probs, 1);

% pca 
p = pca(XTrain, 2500);
% write priciple to file
csvwrite('./pca_vector.csv',p);
XTrain = pcaEmbed(XTrain, p);
XTest = pcaEmbed(XTest, p);


[condProb] = train(XTrain, yTrain, nClass);

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

function [condProb] = train(XTrain, yTrain, nClass)
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

% % remove noise features
% scales = floor(log10(condProb));
% % find max and min scales for each feature
% maxP = max(scales,[],1);
% minP = min(scales,[],1);
% [row, col] = find(maxP ~= minP);
%
%
%XTest = XTest(:, col);
%condProb = condProb(:, col);
end


function [ probs ] = prior( y )

% get the prior probability for each class
% input y is the vector of the training labels
% output the probability of each class
[row, col] = size(y);
count = hist(y, unique(y));
probs = count.'/row;

end

%k is the number of principal components to return.
%P is an f � k matrix containing the first k principal components, 
%where column i contains the ith principal component.
function [ p ] = pca( X, k)

[N, f] = size(X);
p = zeros(f,k);

X = X - ones(N, 1)*mean(X,1);
M = X.' * X / N;
[V, D] = eig(M);
dia = diag(D);
[temp, idice] = sort(dia, 'descend');
p = V(:,idice(1:k));

end


function [ y ] = pcaEmbed( X, P )

y = X * P;

end



