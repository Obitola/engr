% In Class Task Bonus
% File: ML_ACT_Task4.py
% Date: 15 November 2017
% By: Oluwatobi Ola
% olao
% Dave Guo
% guo431
% Section: 3
% Team: 45
%
% ELECTRONIC SIGNATURE
% Oluwatobi Ola
% Dave Guo
%
% The electronic signatures above indicate that the program
% submitted for evaluation is the combined effort of all
% team members and that each member of the team was an
% equal participant in its creation. In addition, each
% member of the team has a general understanding of
% all aspects of the program development and execution.
%
% Works


clear;
clc;
for i = [1:99]
    a(i) = randi(6);
    b(i) = randi(6);
    c(i) = randi(6);
end
d = [a;b;c;];

histogram(d,6);
