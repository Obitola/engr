% In Class Task Bonus
% File: ML_ACT_Task2.py
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

X = -50:0.5:50;
i = 1;
for x = X
    y1(i) = eq1(x);
    y2(i) = eq2(x, 2);
    y3(i) = eq2(x, 5);
    y4(i) = eq2(x, 10);
    y5(i) = eq2(x, 3);
    i = i + 1;
end

f1 = figure;
plot(X,y1,X,y2);
title('Figure 1');
xlabel('X');
ylabel('Y');
legend('Eq1','Eq2');

f2 = figure;
subplot(1,2,1);
plot(X,y1);
title('F(x)');
xlabel('X');
ylabel('Y');
subplot(1,2,2);
plot(X,y3);
title('F(x) A=2');
xlabel('X');
ylabel('Y');

f3 = figure;
plot(X,y1,X,y4);
title('Figure 3');
xlabel('X');
ylabel('Y');
legend('Eq1','Eq2')

f4 = figure;
subplot(2,2,1);
plot(X,y1,X,y4);
title('A=3');
xlabel('X');
ylabel('Y');
legend('Eq1','Eq2')
subplot(2,2,2);
plot(X,y1,X,y4);
title('A=3');
xlabel('X');
ylabel('Y');
legend('Eq1','Eq2')
subplot(2,2,3);
plot(X,y1);
title('A=3');
xlabel('X');
ylabel('Y');
subplot(2,2,4);
plot(X,y4);
title('A=3');
xlabel('X');
ylabel('Y');

function answer = eq1(x)
    a = x;
    b = x.^2/factorial(2);
    c = x.^3/factorial(3);
    d = x.^4/factorial(4);
    answer = 1 + a + b + c + d;
end
function answer = eq2(x, A)
    a = x;
    b = x.^2/factorial(2);
    c = x.^3/factorial(3);
    d = x.^4/factorial(4);
    answer = A * (1 + a + b + c + d);
end
