function [ probs ] = prior( y )

% get the prior probability for each class
% input y is the vector of the training labels
% output the probability of each class
[row, col] = size(y);
count = hist(y, unique(y));
probs = count.'/row;

end

