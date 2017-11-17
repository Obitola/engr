% In Class Task Bonus
% File: ML_ACT_Task3.py
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
t1 = [0:2:10];
for i = [1:6]
    a1(i) = sin(t1(i));
end
figure(1);
plot(t1,a1);
%%
t2 = [0:1:10];
for i = [1:11]
    a2(i) = sin(t2(i));
end
figure(1);
plot(t2,a2);
%%
t3 = [0:0.01:10];
for i = [1:1001];
    a3(i) = sin(t3(i));
end
figure
plot(t1,a1,t2,a2,t3,a3)
