% In Class Task Bonus
% File: ML_ACT_Task4_olao.py
% Date: 29 October 2017
% By: Oluwatobi Ola
% olao
% Dave Guo
% 
% Vivian Guo
% 
% Section: 3
% Team: 45
%
% ELECTRONIC SIGNATURE
% Oluwatobi Ola
% Dave Guo
% Vivian Guo
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

j = 1:100;
for x = j
    rolls(x) = randi(6) + randi(6) + randi(6);
end
disp(rolls);
histogram(rolls,6);