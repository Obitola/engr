% In Class Task Bonus
% File: ML_ACT_Task6_olao.py
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

file = importdata('squat.txt');
time = file.data(:,1);
vastusLateralisRaw = file.data(:,2);
gluteMediusRectified = file.data(:,12);
gluteMediusXYZ = file.data(:,13);
gluteMaxraw = file.data(:,14);
gluteMaxRectified = file.data(:,15);

f1 = figure();
plot(time, vastusLateralisRaw)
title('Vastus Lateralis Raw vs Time');
xlabel('time');
ylabel('Vastus Lateralis Raw');

f2 = figure();
plot(time, gluteMediusRectified)
title('Glute Medius Rectified vs Time');
xlabel('time');
ylabel('Glute medius Rectified');

f3 = figure();
plot(time, gluteMediusXYZ)
title('Glute Medius XYZ vs Time');
xlabel('time');
ylabel('Glute Medius XYZ');

f4 = figure();
plot(time, gluteMaxraw)
title('Glute Max Raw vs Time');
xlabel('time');
ylabel('Glute Max Raw');

f5 = figure();
plot(time, gluteMaxRectified)
title('Glute Max Rectified vs Time');
xlabel('time');
ylabel('Glute Max rectified Z');
