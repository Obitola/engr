% In Class Task Bonus
% File: ML_ACT_Task3_olao.py
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

clear;
clc;

x1 = 0:2:10;
x2 = 0:1:10;
x3 = 0:0.01:10;

i = 1;
for x = x1
    y1(i) = sin(x);
    i = i + 1;
end

i = 1;
for x = x2
    y2(i) = sin(x);
    i = i + 1;
end

i = 1;
for x = x3
    y3(i) = sin(x);
    i = i + 1;
end

plot(x1,y1,x2,y2,x3,y3);
