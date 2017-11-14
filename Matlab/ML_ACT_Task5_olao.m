% In Class Task Bonus
% File: ML_ACT_Task5_olao.py
% Date: 29 October 2017
% By: Oluwatobi Ola
% olao
% Dave Guo
% guo431
% Vivian Guo
% vguo
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

x = input('Which pin package would you like to do? (1: LQFP100 | 2: LQFP144 | 3: QFP176)');
pin = ['LQFP100'; 'LQFP144'; 'LQFP176'];
output = pin(x, :);
