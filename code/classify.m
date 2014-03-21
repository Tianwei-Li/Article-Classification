function [c] = classify(XTrain_fName, yTrain_fName, XTest_fName)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

XTrain = csvread(XTrain_fName);
XTest = csvread(XTest_fName);
yTrain = csvread(yTrain_fName);

% ------ REPLACE WITH YOUR CODE ------
c = zeros(size(XTest,1),1);

end


