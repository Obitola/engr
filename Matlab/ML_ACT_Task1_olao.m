% In Class Task Bonus
% File: ML_ACT_Task1.py
% Date: 15 November 2017
% By: Oluwatobi Ola
% olao
% Dave Guo
% guo431
% Nabeel Khattab
% nalkahtt
% Section: 3
% Team: 45
%
% ELECTRONIC SIGNATURE
% Oluwatobi Ola
% Dave Guo
% Nabeel Khattab
%
% The electronic signatures above indicate that the program
% submitted for evaluation is the combined effort of all
% team members and that each member of the team was an
% equal participant in its creation. In addition, each
% member of the team has a general understanding of
% all aspects of the program development and execution.
%
% Works

clc;
clear;

X = -50:0.1:50;

i = 1;
for x = X
    Y(i) = yplot(x);
    i = i + 1;
end
plot(X, Y);
title('Approximation of sin(x)');
xlabel('X (radians)');
ylabel('Y (sin(x))');

function answer = yplot(x)
    a = x;
    b = -x.^3/factorial(3);
    c = x.^5/factorial(5);
    d = -x.^7/factorial(7);
    answer = a + b + c + d;
end