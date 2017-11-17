% Homework 11: Part 6
% File: HW_11_olao.m
% Date: 17 November 2017
% By: Oluwatobi Ola
% olao
% Section: 3
% Team: 45
%
% ELECTRONIC SIGNATURE
% Oluwatobi Ola
%
% The electronic signature above indicates that the program
% submitted for evaluation is my individual work. I have
% a general understanding of all aspects of its development
% and execution.
%
% A graph of Force vs Distance

clear;
clc;
unit = 1:121;
force = 480:1:600;

i = 1;
for x = force
    d1(i) = distance(x, 0.36);
    d2(i) = distance(x, 0.42);
    i = i + 1;
end

plot(force, d1, force, d2);
xlabel('Force Exerted (N)');
ylabel('Max Distance (m)');
title('Max Distance vs Force Exerted');
legend('Friction Coefficient = 0.36','Friction Coefficient = 0.42');

function answer = distance(force, friction)
    m = 60;
    d = 8;
    g = 9.8;
    angle = pi/6;
    answer = force * d / (m * g * (sin(angle) + cos(angle) * friction));
end